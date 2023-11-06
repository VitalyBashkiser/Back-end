from rest_framework import serializers
from .models import Rating, QuizCompletion, AverageScores, CompanyUsersLastTest


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class QuizCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCompletion
        fields = '__all__'


class AverageScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = AverageScores
        fields = ['quiz', 'average_score', 'date']


class CompanyUsersLastTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUsersLastTest
        fields = '__all__'