from rest_framework import serializers
from .models import Quiz, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    selected_answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'quiz', 'selected_answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'frequency', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz
