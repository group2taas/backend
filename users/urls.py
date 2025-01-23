from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserProfileCreateView

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('profile/user/me', UserProfileCreateView.as_view(), name='create_user_profile'),
]