from django.urls import path
from . import views

urlpatterns = [
    path("", views.PullRequestList.as_view(), name='pull_request_list'),
    path("<uuid:pk>/", views.PullRequestDetails.as_view(), name='pull_request_detail'),
]
