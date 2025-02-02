from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterviewDetailView, QuestionDetailView

# Initialize the DefaultRouter
router = DefaultRouter()

# Define urlpatterns
urlpatterns = [
    path("<int:interview_id>", InterviewDetailView.as_view(), name="interview-detail"),
    path("create", InterviewDetailView.as_view(), name="interview-create"),
    # below exposes the endpoints to interact with the Question model (for development purposes only)
    path(
        "question/<int:question_id>",
        QuestionDetailView.as_view(),
        name="question-detail",
    ),
    path("question", QuestionDetailView.as_view(), name="question-create"),
]
