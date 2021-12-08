from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url

from .views import (
    #GuardianCreateView,
    #GuardianDeleteView,
    GuardianDownloadView,
    GuardianVerifyView,
    GuardianUploadView,
    RecommenderCreateView,
    ParentContestCreateView,
    ParentContestUpdateView,
    ParentContestListView,
    ParentContestDetailView,
    ContestCreateView,
    ContestUpdateView,
    ContestVoteView,
    ContestVoteSuccessView,
    ContestPubkeyView,
    ContestDecryptView,
    ContestOpenView,
    ContestCloseView,
    ContestListView,
    ContestManifestView,
    ContestRecommenderListView,
    ContestRecommenderCreateView,
    ContestRecommenderUpdateView,
    ContestRecommenderDeleteView,
    ContestCandidateListView,
    ContestCandidateCreateView,
    ContestCandidateUpdateView,
    ContestCandidateDeleteView,
    ContestVotersUpdateView,
    ContestVotersDetailView,
    ContestDetailView,
    ContestResultView,
    ContestPublishView,
    EmailVotersView,
)


urlpatterns = [
    #GuardianCreateView.as_url(),
    #GuardianDeleteView.as_url(),
    GuardianDownloadView.as_url(),
    GuardianVerifyView.as_url(),
    GuardianUploadView.as_url(),
    RecommenderCreateView.as_url(),
    ParentContestCreateView.as_url(),
    ParentContestUpdateView.as_url(),
    ParentContestListView.as_url(),
    ParentContestDetailView.as_url(),
    ContestCreateView.as_url(),
    ContestUpdateView.as_url(),
    ContestVoteView.as_url(),
    ContestVoteSuccessView.as_url(),
    ContestPubkeyView.as_url(),
    ContestDecryptView.as_url(),
    ContestOpenView.as_url(),
    ContestCloseView.as_url(),
    ContestListView.as_url(),
    ContestManifestView.as_url(),
    ContestRecommenderListView.as_url(),
    ContestRecommenderCreateView.as_url(),
    ContestRecommenderUpdateView.as_url(),
    ContestRecommenderDeleteView.as_url(),
    ContestCandidateListView.as_url(),
    ContestCandidateCreateView.as_url(),
    ContestCandidateUpdateView.as_url(),
    ContestCandidateDeleteView.as_url(),
    ContestVotersUpdateView.as_url(),
    ContestVotersDetailView.as_url(),
    ContestDetailView.as_url(),
    ContestResultView.as_url(),
    ContestPublishView.as_url(),
    EmailVotersView.as_url(),
]
