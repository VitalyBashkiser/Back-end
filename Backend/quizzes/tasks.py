from celery import shared_task
from django.utils import timezone
from .models import TestResult
from notifications.models import Notification
from django.contrib.auth.models import User


@shared_task
def check_user_quiz_schedule():
    # Get all users
    users = User.objects.all()

    for user in users:
        # Get all the user's test results
        test_results = TestResult.objects.filter(user=user)

        for result in test_results:
            quiz = result.quiz
            last_test_time = result.date_passed

            # Check if enough time has passed since the last test
            if (timezone.now() - last_test_time).days >= quiz.frequency:
                # If enough time has passed, send a notification to the user
                Notification.objects.create(
                    user=user,
                    text=f"It's time to take the quiz: {quiz.title}"
                )