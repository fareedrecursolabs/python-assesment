from django.urls import path
from . import views

urlpatterns = [
    path("<int:repo_id>/", views.BranchList.as_view(), name='branch_list'),
    path("<int:repo_id>/<uuid:pk>/", views.BranchDetails.as_view(), name='branch_detail'),
]
