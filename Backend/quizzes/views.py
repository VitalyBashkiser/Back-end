import logging
import csv
import json
from rest_framework import generics
from .models import Quiz, TestResult, Answer
from .serializers import QuizSerializer, QuestionSerializer
from main.pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from companies.models import Company
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPageNumberPagination


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


@csrf_exempt
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'user', 'company', 'quiz', 'score', 'date passed'])

    for result in TestResult.objects.all():
        writer.writerow([result.id, result.user.username, result.company.name, result.quiz.title, result.score,
                         result.date_passed.strftime("%Y-%m-%d %H:%M:%S")])

    return response


@csrf_exempt
def export_json(request):
    quiz_results = []
    for result in TestResult.objects.all():
        quiz_results.append({
            'id': result.id,
            'user': result.user.username,
            'company': result.company.name,
            'quiz': result.quiz.title,
            'score': result.score,
            'date passed': result.date_passed.strftime("%Y-%m-%d %H:%M:%S")
        })

    json_data = json.dumps(quiz_results, indent=4)

    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response


@api_view(['POST'])
def create_question_with_selected_answers(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()

        # Extract and create associated answers
        answers_data = request.data.get('answers', [])
        for answer_data in answers_data:
            Answer.objects.create(
                question=question,  # This should be the actual question object
                answer_text=answer_data['answer_text'],
                is_correct=answer_data['is_correct']
            )

        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def start_quiz(request, quiz_id):
    get_object_or_404(Quiz, id=quiz_id)
    return Response({'message': 'Quiz started successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def record_test_result(request):
    user_id = request.data.get('user_id')
    company_id = request.data.get('company_id')
    quiz_id = request.data.get('quiz_id')
    score = request.data.get('score')
    correct_answers = request.data.get('correct_answers')

    try:
        user = User.objects.get(id=user_id)
        company = Company.objects.get(id=company_id)
        quiz = Quiz.objects.get(id=quiz_id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Company.DoesNotExist:
        return Response({'error': 'Company does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        TestResult.objects.create(
            user=user,
            company=company,
            quiz=quiz,
            score=score,
            correct_answers=correct_answers
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Test result recorded successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def calculate_average_score(request):
    user_id = request.data.get('user_id')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    total_correct_answers = TestResult.objects.filter(user=user).aggregate(total=Sum('correct_answers'))['total']
    total_questions_answered = TestResult.objects.filter(user=user).aggregate(total=Count('quiz__questions'))['total']

    if total_questions_answered and total_correct_answers:
        average_score = total_correct_answers / total_questions_answered
        return Response({'average_score': average_score}, status=status.HTTP_200_OK)
    else:
        return Response({'average_score': 0}, status=status.HTTP_200_OK)


@login_required
def export_data(request, format):
    user = request.user
    if format == 'json':
        data = TestResult.objects.filter(user=user).values()
        return JsonResponse(list(data), safe=False)
    elif format == 'csv' and (user.is_owner or user.is_administrator):
        data = TestResult.objects.filter(company=user.company)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quiz_results.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'user', 'company', 'quiz', 'score', 'date passed'])
        for result in data:
            writer.writerow([result.id, result.user.username, result.company.name, result.quiz, result.score,
                             result.date_passed])
        return response
    else:
        return HttpResponse("Permission denied", status=403)