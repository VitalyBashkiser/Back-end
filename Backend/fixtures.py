from quizzes.models import Quiz, Question, Answer


def load_fixtures():
    # Quiz 1
    quiz1 = Quiz.objects.create(title='Test Quiz 1', description='This quiz is about capitals', frequency=7)
    question1_1 = Question.objects.create(quiz=quiz1, question_text='What is the capital of France?')
    Answer.objects.create(question=question1_1, answer_text='Paris', is_correct=True)
    Answer.objects.create(question=question1_1, answer_text='London', is_correct=False)
    Answer.objects.create(question=question1_1, answer_text='Berlin', is_correct=False)

    # Quiz 2
    quiz2 = Quiz.objects.create(title='Test Quiz 2', description='This quiz is about animals', frequency=14)
    question2_1 = Question.objects.create(quiz=quiz2, question_text='What is the largest mammal on Earth?')
    Answer.objects.create(question=question2_1, answer_text='Elephant', is_correct=False)
    Answer.objects.create(question=question2_1, answer_text='Blue Whale', is_correct=True)
    Answer.objects.create(question=question2_1, answer_text='Giraffe', is_correct=False)

    # Quiz 3
    quiz3 = Quiz.objects.create(title='Test Quiz 3', description='This quiz is about capitals again', frequency=30)
    question3_1 = Question.objects.create(quiz=quiz3, question_text='What is the capital of Japan?')
    Answer.objects.create(question=question3_1, answer_text='Tokyo', is_correct=True)
    Answer.objects.create(question=question3_1, answer_text='Beijing', is_correct=False)
    Answer.objects.create(question=question3_1, answer_text='Seoul', is_correct=False)


load_fixtures()
