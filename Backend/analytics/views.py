from rest_framework import generics, permissions
from .models import Rating, QuizCompletion, AverageScores
from .serializers import RatingSerializer, QuizCompletionSerializer, AverageScoresSerializer,\
    CompanyUsersLastTestSerializer
from companies.models import Company
from main.models import User


class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class QuizCompletionListView(generics.ListCreateAPIView):
    serializer_class = QuizCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QuizCompletion.objects.filter(user=user)


class AverageScoresListView(generics.ListAPIView):
    queryset = AverageScores.objects.all()
    serializer_class = AverageScoresSerializer


class UserAverageScoresListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AverageScoresSerializer


class UserQuizAverageScoresListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AverageScoresSerializer


class CompanyUsersLastTestListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUsersLastTestSerializer
