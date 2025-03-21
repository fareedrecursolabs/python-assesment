from django.urls import path
from . import views

urlpatterns = [
    path("", views.RepoList.as_view(), name='repo_list'),
    path("<int:pk>/", views.RepoDetails.as_view(), name='repo_detail'),
]
