from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from activities.models import Activity
from .services import calculate_vu, get_vu_distribution


class CalculateVUView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id, user=request.user)
        except Activity.DoesNotExist:
            return Response(
                {'error': 'Activity not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if activity.status != 'verified':
            return Response(
                {'error': 'Activity must be verified before VU calculation'},
                status=status.HTTP_400_BAD_REQUEST
            )

        maintenance_count = activity.maintenance_logs.filter(
            plant_health=True
        ).count()

        total_vu = calculate_vu(activity, maintenance_count)
        distribution = get_vu_distribution(total_vu)

        # Save to activity
        activity.total_vu = distribution['total_vu']
        activity.released_vu = distribution['initial_release']
        activity.locked_vu = distribution['locked_vu']
        activity.save()

        # Update user total VU
        user = request.user
        user.total_vu += distribution['initial_release']
        user.trees_planted += 1
        user.save()

        return Response({
            'message': 'VU calculated successfully',
            'activity_id': activity.id,
            'plant_species': activity.plant_species,
            'vu_breakdown': {
                'impact_potential': activity.plant_species,
                'total_vu': distribution['total_vu'],
                'released_now': distribution['initial_release'],
                'locked_vu': distribution['locked_vu'],
                'checkpoint_distribution': distribution['checkpoint_distribution'],
            }
        }, status=status.HTTP_200_OK)


class VUSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        activities = Activity.objects.filter(user=user)

        activity_data = []
        for activity in activities:
            activity_data.append({
                'id': activity.id,
                'plant_species': activity.plant_species,
                'status': activity.status,
                'total_vu': activity.total_vu,
                'released_vu': activity.released_vu,
                'locked_vu': activity.locked_vu,
            })

        return Response({
            'user': user.username,
            'total_vu': user.total_vu,
            'trees_planted': user.trees_planted,
            'activities': activity_data,
        })