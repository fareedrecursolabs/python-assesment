from django.urls import path
from . import views

urlpatterns = [
    path("<uuid:branch_id>/", views.CommitsView.as_view(), name='commits_list'),
    path("<uuid:branch_id>/<uuid:pk>/", views.CommitViewById.as_view(), name='commits_detail'),
]
