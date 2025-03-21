from .serializer import CommitsSerializer
from rest_framework import generics
from .models import Commit

class CommitsView(generics.ListAPIView):
  serializer_class = CommitsSerializer

  def get_queryset(self):
    branch_id = self.kwargs['branch_id']
    return Commit.objects.filter(branch=branch_id)
