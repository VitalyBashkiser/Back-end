import logging
from rest_framework import generics
from .models import Quiz, TestResult
from .serializers import QuizSerializer, QuestionSerializer
from main.pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum, Count


logger = logging.getLogger(__name__)


class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPageNumberPagination


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class RecordTestResult(APIView):
    def post(self, request, format=None):
        # Get user, company, quiz, score, and correct_answers from request data
        user_id = request.data.get('user_id')
        company_id = request.data.get('company_id')
        quiz_id = request.data.get('quiz_id')
        score = request.data.get('score')
        correct_answers = request.data.get('correct_answers')

        # Create a new TestResult object
        test_result = TestResult.objects.create(
            user_id=user_id,
            company_id=company_id,
            quiz_id=quiz_id,
            score=score,
            correct_answers=correct_answers
        )

        # Calculate the average score and update it for the user
        user = User.objects.get(id=user_id)
        total_correct_answers = TestResult.objects.filter(user=user).aggregate(total=Sum('correct_answers'))['total']
        total_questions_answered = TestResult.objects.filter(user=user).aggregate(total=Sum('quiz__questions__count'))[
            'total']

        if total_questions_answered and total_correct_answers:
            average_score = total_correct_answers / total_questions_answered
            user.profile.average_score = average_score
            user.profile.save()

        return Response({'message': 'Test result recorded successfully'}, status=status.HTTP_201_CREATED)


def calculate_average_score(user):
    total_correct_answers = TestResult.objects.filter(user=user).aggregate(total=Sum('correct_answers'))['total']
    total_questions_answered = TestResult.objects.filter(user=user).aggregate(total=Count('quiz__questions'))['total']

    if total_questions_answered and total_correct_answers:
        average_score = total_correct_answers / total_questions_answered
        return average_score
    else:
        return 0


def expected_average_score(total_correct_answers, total_questions_answered):
    if total_questions_answered and total_correct_answers:
        average_score = total_correct_answers / total_questions_answered
        return average_score
    else:
        return 0


@api_view(['POST'])
def create_question_with_selected_answers(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return Response({'message': 'Quiz started successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def record_test_result(request):
    user_id = request.data.get('user_id')
    company_id = request.data.get('company_id')
    quiz_id = request.data.get('quiz_id')
    score = request.data.get('score')

    test_result = TestResult.objects.create(user_id=user_id, company_id=company_id, quiz_id=quiz_id, score=score)

    return Response({'message': 'Test result recorded successfully'}, status=status.HTTP_201_CREATED)
