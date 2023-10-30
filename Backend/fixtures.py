from quizzes.models import Quiz, Question, Answer


def create_question_with_selected_answers(quiz, question_text, answers):
    question = Question.objects.create(quiz=quiz, question_text=question_text)
    for answer in answers:
        Answer.objects.create(question=question, **answer)


quiz1 = Quiz.objects.create(title='Test Quiz 1', description='Description 1', frequency=7)
quiz2 = Quiz.objects.create(title='Test Quiz 2', description='Description 2', frequency=7)
quiz3 = Quiz.objects.create(title='Test Quiz 3', description='Description 3', frequency=7)

questions_data = [
    {
        "quiz": quiz1,
        "question_text": "What is the capital of France?",
        "answers": [
            {"answer_text": "Paris", "is_correct": True},
            {"answer_text": "London", "is_correct": False},
            {"answer_text": "Berlin", "is_correct": False}
        ]
    },
    {
        "quiz": quiz2,
        "question_text": "What is the largest mammal on Earth?",
        "answers": [
            {"answer_text": "Elephant", "is_correct": False},
            {"answer_text": "Blue Whale", "is_correct": True},
            {"answer_text": "Giraffe", "is_correct": False}
        ]
    },
    {
        "quiz": quiz3,
        "question_text": "What is the capital of Japan?",
        "answers": [
            {"answer_text": "Tokyo", "is_correct": False},
            {"answer_text": "Beijing", "is_correct": True},
            {"answer_text": "Seoul", "is_correct": False}
        ]
    }
]

for question_data in questions_data:
    create_question_with_selected_answers(**question_data)