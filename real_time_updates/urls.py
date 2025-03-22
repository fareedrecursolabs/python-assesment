from django.urls import path
from . import views

urlpatterns = [
    path('stream/commit/<uuid:branch_id>/', views.sse_stream, name='sse_stream'),
]
