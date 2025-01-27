from django.shortcuts import render
from rest_framework.response import Response
from firebase_admin import credentials, auth
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from loguru import logger

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserProfileSerializer
import core.firebase


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.request.user.pk)


class FirebaseLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = self._extract_token(request)
        if not id_token:
            return Response(
                {"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get("user_id")

            user = UserProfile.objects.get(uid=uid)

            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def _extract_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return request.data.get("idToken")


class FirebaseSignupView(APIView):
    serializer_class = UserProfileSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = self._extract_token(request)
        print(id_token)
        if not id_token:
            return Response(
                {"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_token = auth.verify_id_token(id_token)

            uid = decoded_token.get("user_id")
            email = decoded_token.get("email")

            user_data = request.data.get("user", {})

            user, created = UserProfile.objects.get_or_create(
                uid=uid,
                defaults={
                    "email": email,
                    "name": user_data.get("name", "Anonymous"),
                    "phone": user_data.get("phone", ""),
                    "company_name": user_data.get("company_name", ""),
                },
            )

            if not created:
                return Response(
                    {"error": "User already exists"}, status=status.HTTP_409_CONFLICT
                )

            refresh = RefreshToken.for_user(user)
            print(str(refresh.access_token))
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.info(f"Firebase token error : {e}")
            return Response(
                {"error": "Registration failed"}, status=status.HTTP_400_BAD_REQUEST
            )

    def _extract_token(self, request):
        return request.data.get("idToken")
