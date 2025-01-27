from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserProfileView, FirebaseLoginView, FirebaseSignupView

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include router-generated URLs
    path('profile/me/', UserProfileView.as_view(), name='user_profile'),
    path('login/', FirebaseLoginView.as_view(), name='firebase-login'),
    path('signup/', FirebaseSignupView.as_view(), name='firebase-signup'),
]