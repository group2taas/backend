from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultCreateView, ResultPDFView, AllResultsView

# Initialize the DefaultRouter
router = DefaultRouter()

# Define urlpatterns
urlpatterns = [
    path("", AllResultsView.as_view(), name="result_list"),
    path("upload", ResultCreateView.as_view(), name="upload_result"),
    path("<int:ticket_id>", ResultCreateView.as_view()),
    path("<int:result_id>/pdf", ResultPDFView.as_view()),
]
