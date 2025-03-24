from django.shortcuts import render
from rest_framework import generics
from .models import Branch
from .serializer import BranchSerializer

# Create your views here.
class BranchList(generics.ListAPIView):
  serializer_class = BranchSerializer

  def get_queryset(self):
    repo_id = self.kwargs['repo_id']
    return Branch.objects.filter(repo=repo_id)



class BranchDetails(generics.RetrieveAPIView):
  serializer_class = BranchSerializer

  def get_queryset(self):
    repo_id = self.kwargs.get("repo_id")
    branch_id = self.kwargs.get("pk")
    return Branch.objects.filter(repo=repo_id, id=branch_id)
