from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultCreateView, ResultPDFView, AllResultsView, TicketResultView, EmbedPDFView
from django.conf import settings
from django.conf.urls.static import static

# Initialize the DefaultRouter
router = DefaultRouter()

# Define urlpatterns
urlpatterns = [
    path("", AllResultsView.as_view(), name="result_list"),
    path("upload", ResultCreateView.as_view(), name="upload_result"),
    path("<int:result_id>", ResultCreateView.as_view()),
    path("<int:result_id>/pdf", ResultPDFView.as_view()),
    path("ticket/<int:ticket_id>", TicketResultView.as_view(), name="result_by_ticket"),
    path("embed-pdf/<int:result_id>/<str:filename>/", EmbedPDFView.as_view(), name="embed_pdf"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
