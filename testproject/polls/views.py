
import datetime
from django.core.exceptions import EmptyResultSet
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

from .models import Poll, Question, Answer, Choice
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer


class PollView(viewsets.ViewSet):

    """
    Polls ViewSet that for listing or retrieving questions.
    """

    def list(self, request):
        queryset = Poll.objects.filter(end__gt=datetime.datetime.now())
        serializer = PollSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Poll.objects.all()
        question = get_object_or_404(queryset, pk=pk)
        serializer = PollSerializer(question)
        return Response(serializer.data)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = PollSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs.get("user")
        if user and user.is_staff:
            return Poll.objects.all()
        return Poll.objects.filter(end__gt=datetime.datetime.now())


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self, *args, **kwargs):
        poll_id = self.kwargs.get("poll_pk")
        try:
            poll = Poll.objects.get(pk=poll_id)
        except poll.DoesNotExist:
            raise NotFound('A poll with this id does not exist')
        return self.queryset.filter(poll=poll)


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def get_queryset(self, *args, **kwargs):
        question_id = self.kwargs.get("question_pk")
        try:
            question = Question.objects.get(pk=question_id)
        except question.DoesNotExist:
            raise NotFound('A question with this id does not exist')
        return self.queryset.filter(question=question_id)


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer

    def get_queryset(self, *args, **kwargs):
        return Choice.objects.all()


class ChoiceUserViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        try:
            choices = Choice.objects.filter(user_id=user_id)
            if not choices:
                raise EmptyResultSet
        except EmptyResultSet:
            raise NotFound('A choices with this user_id does not exist')
        return choices
