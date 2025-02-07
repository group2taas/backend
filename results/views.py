from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .models import Result
from .serializers import ResultSerializer

from django.http import FileResponse


# TODO: abstract the following into a custom BasePermission class (same for other views)
def _check_user_permission(request, result):
    if result.ticket.user.pk != request.user.pk:
        return Response(
            {"error": "Result does not belong to user"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class AllResultsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer

    def get_queryset(self):
        return Result.objects.filter(ticket__user=self.request.user)


class ResultCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResultSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def get(self, request, result_id):
        result = get_object_or_404(Result, pk=result_id)
        _check_user_permission(request, result)
        serializer = ResultSerializer(result, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, result_id):
        result = get_object_or_404(Result, pk=result_id)
        _check_user_permission(request, result)
        pdf_path = result.pdf.path
        return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
