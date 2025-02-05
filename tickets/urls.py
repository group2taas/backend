from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketCreateView, AllTicketsView, TicketDetailView

# Initialize the DefaultRouter
router = DefaultRouter()

# Define urlpatterns
urlpatterns = [
    path("create", TicketCreateView.as_view(), name="create_ticket"),
    path("<int:ticket_id>", TicketDetailView.as_view(), name="ticket_detail"),
    path("", AllTicketsView.as_view(), name="ticket_list"),
]
