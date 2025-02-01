from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, status
from .models import Result
from .serializers import ResultSerializer

from django.http import FileResponse


class AllResultsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer

    def get_queryset(self):
        return Result.objects.filter(ticket__user=self.request.user)


class ResultCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, result_id):
        result = get_object_or_404(Result, pk=result_id)
        if result.ticket.user.id != request.user.pk:
            return Response(
                {"error": "Result does not belong to user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, result_id):
        result = get_object_or_404(Result, pk=result_id)
        if result.ticket.user.id != request.user.pk:
            return Response(
                {"error": "Result does not belong to user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        pdf_path = result.pdf.path
        return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
