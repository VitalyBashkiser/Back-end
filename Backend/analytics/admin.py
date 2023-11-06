from django.contrib import admin
from django.db.models import Sum
from quizzes.models import Quiz
from main.models import User
from .models import Rating, QuizCompletion, AverageScores, CompanyUsersLastTest


# [ ] Rating is also the general Average score for all quizzes from all companies as a whole (anyone can watch this)
def get_general_average_score():
    total_ratings = Rating.objects.count()
    if total_ratings > 0:
        total_score = Rating.objects.aggregate(total_score=Sum('average_score'))['total_score']
        return total_score / total_ratings
    return None


# [ ] List of quizzes and the time if it’s last completions.
# Only owner and administrators of companies should be able to receive the that data
def get_quiz_completion_time(owner_id):
    if owner_id is not None:
        quizzes = QuizCompletion.objects.filter(user__company__owner=owner_id)
        quiz_times = {}
        for quiz in quizzes:
            if quiz.quiz.title not in quiz_times or quiz.completion_time > quiz_times[quiz.quiz.title]:
                quiz_times[quiz.quiz.title] = quiz.completion_time
        return quiz_times
    return None


# [ ] List of average scores for each of the quiz from all companies with dynamics over time
def get_average_scores_by_quiz():
    quizzes = Quiz.objects.all()
    average_scores = []
    for quiz in quizzes:
        scores = AverageScores.objects.filter(quiz=quiz)
        scores_data = [(score.date, score.average_score) for score in scores]
        average_scores.append({
            'quiz_title': quiz.title,
            'scores_data': scores_data
        })
    return average_scores


# [ ] List of average scores of all users with dynamics over time
def get_average_scores_by_user():
    users = User.objects.all()
    average_scores = []
    for user in users:
        scores = Rating.objects.filter(user=user)
        scores_data = [(score.date, score.average_score) for score in scores]
        average_scores.append({
            'user_username': user.username,
            'scores_data': scores_data
        })
    return average_scores


# [ ] List of average scores for all quizzes of the selected user with dynamics over time
def get_average_scores_by_user_quizzes(user_id):
    user = User.objects.get(id=user_id)
    quizzes = Quiz.objects.all()
    user_scores = []
    for quiz in quizzes:
        scores = Rating.objects.filter(user=user, quiz=quiz)
        scores_data = [(score.date, score.average_score) for score in scores]
        user_scores.append({
            'quiz_title': quiz.title,
            'scores_data': scores_data
        })
    return user_scores


# [ ] List of users of the company and their time of last test
def get_users_last_test_time(company_id):
    users_last_tests = CompanyUsersLastTest.objects.filter(company=company_id)
    users_data = []
    for user_last_test in users_last_tests:
        users_data.append({
            'user_username': user_last_test.user.username,
            'last_test_time': user_last_test.last_test_time
        })
    return users_data


admin.site.register(Rating)
admin.site.register(QuizCompletion)
admin.site.register(AverageScores)
admin.site.register(CompanyUsersLastTest)
