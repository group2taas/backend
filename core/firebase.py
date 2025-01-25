import firebase_admin
from firebase_admin import credentials, auth
from rest_framework import authentication
from users.models import UserProfile

from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError

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
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken
        if not id_token or not decoded_token:
            return None
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError
        try:
            user = UserProfile.objects.get(pk=uid)
        except:
            raise authentication.AuthenticationFailed("No such user")

        return (user, None)
