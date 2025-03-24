from django.urls import path
from . import views

urlpatterns = [
    path("<int:repo_id>/", views.PullRequestList.as_view(), name='pull_request_list'),
    path("<int:repo_id>/<uuid:pk>/", views.PullRequestDetails.as_view(), name='pull_request_detail'),
]
