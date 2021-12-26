from django.urls import path, include
from rest_framework_nested import routers

from .views import PollViewSet, QuestionViewSet, AnswerViewSet, ChoiceViewSet, ChoiceUserViewSet

router = routers.SimpleRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'choices', ChoiceViewSet, basename='choice')
router.register(r'(?P<user_id>.+)/choices', ChoiceUserViewSet, basename='choice')

question_router = routers.NestedSimpleRouter(
    router,
    r'polls',
    lookup='poll'
)

question_router.register(
    r'questions',
    QuestionViewSet,
    basename='poll-question'
)

answer_router = routers.NestedSimpleRouter(
    question_router,
    r'questions',
    lookup='question'
)

answer_router.register(
    r'answers',
    AnswerViewSet,
    basename='question-answer'
)

app_name = 'polls'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(question_router.urls)),
    path('', include(answer_router.urls)),

]
