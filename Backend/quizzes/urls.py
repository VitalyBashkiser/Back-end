from django.urls import path
from .views import QuizListView, QuizDetailView, start_quiz, create_result, create_question_with_selected_answers

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/create_question/', create_question_with_selected_answers,
         name='create_question_with_selected_answers'),
    path('quizzes/start-quiz/<int:quiz_id>/', start_quiz, name='start-quiz'),
    path('quizzes/create_result/', create_result, name='create_result'),
]
