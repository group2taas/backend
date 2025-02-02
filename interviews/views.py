from core import settings
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .models import Interview, Question, Answer
from .serializers import InterviewSerializer, QuestionSerializer, AnswerSerializer


# TODO: abstract the following into a custom BasePermission class (same for other views)
def _check_user_permission(request, interview):
    if not settings.DEBUG:
        if interview.ticket.user.pk != request.user.pk:
            return Response(
                {"error": "Response does not belong to user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class InterviewDetailView(APIView):
    permission_classes = [AllowAny] if settings.DEBUG else [IsAuthenticated]

    def get(self, request, interview_id):
        interview = get_object_or_404(Interview, pk=interview_id)
        _check_user_permission(request, interview)
        serializer = InterviewSerializer(interview)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, interview_id):
        interview = get_object_or_404(Interview, pk=interview_id)
        _check_user_permission(request, interview)
        serializer = InterviewSerializer(interview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
