from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Recognition
from .serializers import RecognitionSerializer
from .services import check_and_award_badges, update_urban_forest_score, get_leaderboard


class CheckBadgesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        newly_awarded = check_and_award_badges(user)
        update_urban_forest_score(user)

        all_badges = Recognition.objects.filter(user=user)
        serializer = RecognitionSerializer(all_badges, many=True)

        return Response({
            'message': f'{len(newly_awarded)} new badge(s) awarded!',
            'newly_awarded': newly_awarded,
            'all_badges': serializer.data,
            'urban_forest_score': user.urban_forest_score,
        })


class UserBadgesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        badges = Recognition.objects.filter(user=user)
        serializer = RecognitionSerializer(badges, many=True)

        return Response({
            'username': user.username,
            'urban_forest_score': user.urban_forest_score,
            'trees_planted': user.trees_planted,
            'trees_survived_one_year': user.trees_survived_one_year,
            'total_vu': user.total_vu,
            'badges': serializer.data,
        })


class LeaderboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        leaderboard = get_leaderboard()
        return Response({
            'leaderboard': leaderboard
        })