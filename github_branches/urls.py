from django.urls import path
from . import views

urlpatterns = [
    path("", views.BranchList.as_view(), name='branch_list'),
    path("<uuid:pk>/", views.BranchDetails.as_view(), name='branch_detail'),
]
