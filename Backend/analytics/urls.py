from django.urls import path
from .views import (
    RatingListView,
    QuizCompletionListView,
    AverageScoresListView,
    UserAverageScoresListView,
    UserQuizAverageScoresListView,
    CompanyUsersLastTestListView
)

urlpatterns = [
    path('ratings/', RatingListView.as_view(), name='rating-list'),
    path('quizzes/completions/', QuizCompletionListView.as_view(), name='quizcompletion-list'),
    path('average_scores/quizzes/', AverageScoresListView.as_view(), name='quiz-averagescores-list'),
    path('average_scores/users/', UserAverageScoresListView.as_view(), name='user-averagescores-list'),
    path('average_scores/user/<int:user_id>/quizzes/', UserQuizAverageScoresListView.as_view(), name='user-quiz-averagescores-list'),
    path('company_users_last_test/', CompanyUsersLastTestListView.as_view(), name='company-users-lasttest-list'),
]