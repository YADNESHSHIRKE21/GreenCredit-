from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from activities.models import Activity
from .models import MaintenanceLog
from .serializers import MaintenanceLogSerializer
from .services import get_due_checkpoint, process_maintenance_submission


class MaintenanceSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id, user=request.user)
        except Activity.DoesNotExist:
            return Response(
                {'error': 'Activity not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if activity.status not in ['verified', 'completed']:
            return Response(
                {'error': 'Activity must be verified first'},
                status=status.HTTP_400_BAD_REQUEST
            )

        checkpoint_day = get_due_checkpoint(activity)
        if checkpoint_day is None:
            return Response(
                {'error': 'No checkpoint due at this time'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gps_data = request.data.get('gps_location')
        image = request.FILES.get('image')

        if not gps_data or not image:
            return Response(
                {'error': 'GPS location and image are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = process_maintenance_submission(
            activity, checkpoint_day, gps_data, image
        )

        if results['passed']:
            log = MaintenanceLog.objects.create(
                activity=activity,
                day_checkpoint=checkpoint_day,
                image=image,
                gps_location=gps_data,
                plant_health=True,
                vu_released=results['vu_released']
            )
            return Response({
                'message': f'Day {checkpoint_day} checkpoint verified!',
                'vu_released': results['vu_released'],
                'remaining_locked_vu': activity.locked_vu,
                'results': results
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Maintenance verification failed',
                'results': results
            }, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id, user=request.user)
        except Activity.DoesNotExist:
            return Response(
                {'error': 'Activity not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        logs = MaintenanceLog.objects.filter(activity=activity)
        serializer = MaintenanceLogSerializer(logs, many=True)

        due_checkpoint = get_due_checkpoint(activity)

        return Response({
            'activity_id': activity_id,
            'status': activity.status,
            'total_vu': activity.total_vu,
            'released_vu': activity.released_vu,
            'locked_vu': activity.locked_vu,
            'next_checkpoint': due_checkpoint,
            'completed_checkpoints': [log['day_checkpoint'] for log in serializer.data],
            'logs': serializer.data
        })