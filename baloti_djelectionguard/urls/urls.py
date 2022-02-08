from django.urls import path
from ..views import *

urlpatterns = [
    path('', BalotiIndexView.as_view()),
    path('contest/list/', BalotiContestListView.as_view()),
    path('contest/list/<str:sort>', BalotiContestListSortView.as_view(), name='ContestSortedList'),
    path('contest/<str:id>', BalotiContestDetailView.as_view(), name='ContestDetails'),
    path('contest/vote/choices/<str:id>', BalotiContestChoicesView.as_view(), name='VoteChoices'),
    path('vote/<str:id>', VoteView.as_view(), name='casteVote'),
    path('contest/detail/<str:id>', BalotiContestDetailView.as_view(), name='viewContestDetails'),
    path('contest/result/<str:id>', BalotiContestResultView.as_view(), name='viewContestResult'),
    path('anonymous/vote/', BalotiAnonymousVoteView.as_view(), name='anonymousVote'),
    path('contest/vote/success/<str:id>', VoteSuccessView.as_view(), name='VoteSuccess'),
]
