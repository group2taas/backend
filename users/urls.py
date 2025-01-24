from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserProfileCreateView

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include router-generated URLs
    path('profile/user/me', UserProfileCreateView.as_view(), name='create_user_profile'),
]