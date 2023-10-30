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
    path('analytics/ratings/', RatingListView.as_view(), name='rating-list'),
    path('analytics/quizcompletions/', QuizCompletionListView.as_view(), name='quizcompletion-list'),
    path('analytics/average_scores/quizzes/', AverageScoresListView.as_view(), name='quiz-averagescores-list'),
    path('analytics/average_scores/users/', UserAverageScoresListView.as_view(), name='user-averagescores-list'),
    path('analytics/average_scores/user/<int:user_id>/quizzes/', UserQuizAverageScoresListView.as_view(),
         name='user-quiz-averagescores-list'),
    path('analytics/company_users_last_test/', CompanyUsersLastTestListView.as_view(),
         name='company-users-lasttest-list'),
]