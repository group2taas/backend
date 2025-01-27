import firebase_admin
from firebase_admin import credentials, auth
from rest_framework import authentication
from users.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError
from loguru import logger

cred = credentials.Certificate("core/firebase_config.json")
firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=60)
        except Exception:
            raise InvalidAuthToken
        if not id_token or not decoded_token:
            return None
        try:
            uid = decoded_token.get("user_id")
            user, created = UserProfile.objects.get_or_create(
                uid=uid,
                defaults={
                    "email": decoded_token.get("email"),
                    "name": decoded_token.get("name", "Anonymous"),
                }
            )
        except Exception:
            raise FirebaseError

        user = get_object_or_404(UserProfile, pk=uid)

        refresh = RefreshToken.for_user(user)
        user.jwt = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return (user, None)
