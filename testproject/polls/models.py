import datetime

from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название опроса")
    start = models.DateTimeField(auto_now=True, editable=False, verbose_name="start date")
    end = models.DateTimeField(editable=True, verbose_name="Дата завершения")
    description = models.TextField(max_length=400, verbose_name="Описание")

    def __str__(self):
        return "Опрос: " + self.name + ". id: " + str(self.pk)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Question(models.Model):
    TEXT = "TEXT ANSWER"
    SINGLE = "SINGLE ANSWER"
    PLURAL = "PLURAL ANSWER"

    TYPE_CHOICES = [
        (TEXT, "Текстовый ответ"),
        (SINGLE, "Один правильный ответ"),
        (PLURAL, "Много правильных ответов"),
    ]

    text = models.CharField(max_length=1000, verbose_name="Вопрос")
    type = models.CharField(max_length=13, choices=TYPE_CHOICES, default=TEXT, verbose_name="Тип ответа")
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return "Вопрос:  " + self.text + " Тип ответа - " + self.type + " id: " + str(self.pk)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name="Ответ")
    question = models.ForeignKey(
        Question, related_name="answers",
        on_delete=models.CASCADE, verbose_name="Вопрос"
    )
    is_right = models.BooleanField(verbose_name="Правильный ответ")

    def __str__(self):
        return "Ответ: " + self.text + ". id: " + str(self.pk)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Choice(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True, verbose_name="Текст ответа")
    answer_id = models.ForeignKey(Answer, blank=True, null=True, verbose_name="Номер ответа", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    user_id = models.IntegerField(verbose_name="Номер пользователя")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def __str__(self):
        return "Ответ пользователя " + str(self.user_id) + " на " + str(self.question)
