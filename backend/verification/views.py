from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from activities.models import Activity
from .services import verify_activity


class VerifyActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id, user=request.user)
        except Activity.DoesNotExist:
            return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

        if activity.status != 'pending':
            return Response({'error': 'Activity already processed'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = activity.initial_image if activity.initial_image else None
        results = verify_activity(activity, image_file)

        if results['passed']:
            activity.status = 'verified'
            activity.save()
            return Response({
                'message': 'Activity verified successfully',
                'results': results
            }, status=status.HTTP_200_OK)
        else:
            activity.status = 'rejected'
            activity.save()
            return Response({
                'message': 'Activity verification failed',
                'results': results
            }, status=status.HTTP_400_BAD_REQUEST)


class VerificationStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id, user=request.user)
        except Activity.DoesNotExist:
            return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'activity_id': activity.id,
            'status': activity.status,
            'plant_species': activity.plant_species,
            'timestamp': activity.timestamp
        })