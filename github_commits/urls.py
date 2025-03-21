from django.urls import path
from . import views

urlpatterns = [
    path("<uuid:branch_id>/", views.CommitsView.as_view(), name='commits_list'),
]
