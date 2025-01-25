from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .models import Ticket
from .serializers import TicketSerializer

from core.firebase import FirebaseAuthentication
from users.models import UserProfile


class AllTicketsView(ListAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    # TODO: include filtering and ordering
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(UserProfile, pk=uid)

        return Ticket.objects.all().filter(user=user)


class TicketCreateView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        uid = request.user.id
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        if ticket.user.id != uid:
            return Response(
                {"error": "Ticket does not belong to user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
