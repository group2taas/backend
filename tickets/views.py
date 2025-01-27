from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, status
from .models import Ticket
from .serializers import TicketSerializer

from users.models import UserProfile


def _extract_user(request):
    token = request.headers.get("Authorization")
    token = AccessToken(token.split(" ")[1])
    return token["uid"]


class AllTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    # TODO: include filtering and ordering
    def get_queryset(self):
        uid = _extract_user(self.request)
        get_object_or_404(UserProfile, pk=uid)

        return Ticket.objects.all().filter(user=uid)


class TicketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        uid = _extract_user(request)
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        if ticket.user.uid != uid:
            return Response(
                {"error": "Ticket does not belong to user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["user"] = _extract_user(request)
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        uid = _extract_user(request)
        if ticket.user.uid != uid:
            return Response(
                {"error": "Ticket does not belong to user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
