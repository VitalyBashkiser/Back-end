from django.urls import path
from .views import QuizListView, QuizDetailView, create_question_with_selected_answers

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/create_question/', create_question_with_selected_answers,
         name='create_question_with_selected_answers'),
]
