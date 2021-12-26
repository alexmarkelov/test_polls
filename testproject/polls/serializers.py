from rest_framework import serializers

from .models import Poll, Question, Answer, Choice


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('text', 'question', 'is_right', 'pk')

    def create(self, validated_data):
        question = Question.objects.get(pk=self.context["view"].kwargs["question_pk"])
        validated_data["question"] = question
        return Answer.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Question
        fields = ('text', 'type', 'poll', 'answers', 'pk')

    def create(self, validated_data):
        poll = Poll.objects.get(pk=self.context["view"].kwargs["poll_pk"])
        validated_data["poll"] = poll
        return Question.objects.create(**validated_data)


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Poll
        fields = ('name', 'start', 'end', 'description', 'questions', 'pk')

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('text', 'answer_id', 'question', 'user_id', 'pk')

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)
