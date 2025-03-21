from rest_framework import generics
from .serializer import PullRequestSerializer
from .models import PullRequest

class PullRequestList(generics.ListAPIView):
  serializer_class = PullRequestSerializer
  queryset = PullRequest.objects.all()

class PullRequestDetails(generics.RetrieveAPIView):
  serializer_class = PullRequestSerializer
  queryset = PullRequest.objects.all()
