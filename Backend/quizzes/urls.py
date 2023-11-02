from django.urls import path
from .views import QuizListView, QuizDetailView, start_quiz, create_result, export_json,\
    create_question_with_selected_answers, export_csv

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/question/1/', create_question_with_selected_answers, name='question_test_1'),
    path('quizzes/question/2/', create_question_with_selected_answers, name='question_test_2'),
    path('quizzes/question/3/', create_question_with_selected_answers, name='question_test_3'),
    path('quizzes/start-quiz/<int:quiz_id>/', start_quiz, name='start-quiz'),
    path('quizzes/create_result/', create_result, name='create_result'),
    path('quizzes/export-csv/', export_csv, name='export-csv'),
    path('quizzes/export-json/', export_json, name='export-json'),
]
