from rest_framework import generics
from .serializer import PullRequestSerializer
from .models import PullRequest

class PullRequestList(generics.ListAPIView):
  serializer_class = PullRequestSerializer
  def get_queryset(self):
    repo_id = self.kwargs['repo_id']
    return PullRequest.objects.filter(repo=repo_id)

class PullRequestDetails(generics.RetrieveAPIView):
  serializer_class = PullRequestSerializer
  def get_queryset(self):
    repo_id = self.kwargs.get("repo_id")
    pull_request_id = self.kwargs.get("pk")
    return PullRequest.objects.filter(repo=repo_id, id=pull_request_id)
