from rest_framework import generics
from .models import Quiz, Answer
from .serializers import QuizSerializer, QuestionSerializer
from main.pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPageNumberPagination


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


@api_view(['POST'])
def create_question_with_selected_answers(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()

        # Extract and create associated answers
        answers_data = request.data.get('answers', [])
        for answer_data in answers_data:
            Answer.objects.create(
                question_ref=question,
                answer_text=answer_data['answer_text'],
                is_correct=answer_data['is_correct']
            )

        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



