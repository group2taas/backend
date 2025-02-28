from rest_framework import serializers
from .models import Ticket
from interviews.serializers import InterviewSerializer
from results.serializers import ResultSerializer

class TicketSerializer(serializers.ModelSerializer):
    interview = InterviewSerializer(read_only=True)
    result =  ResultSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = "__all__"
