from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    alerts_summary = serializers.SerializerMethodField()
    pdf_link = serializers.SerializerMethodField()
    class Meta:
        model = Result
        fields = [
            'id', 
            'title', 
            'created_at', 
            'ticket', 
            'logs', 
            'progress', 
            'pdf',
            'security_alerts',
            'alerts_detail',
            'alerts_summary',
            'num_tests',
            'pdf_link'
        ]
        read_only_fields = ['logs', 'progress', 'security_alerts', 'alerts_detail']
    
    def get_alerts_summary(self, obj):
        counts = obj.get_alert_counts()
        total = sum(counts.values())
        return {
            "counts": counts,
            "total": total
        }
    
    # TODO: to be determined based on how the pdf is stored
    def get_pdf_link(self, obj):
        if obj.pdf:
            return str(obj.pdf.url)
        else:
            return None

    def validate_ticket(self, ticket):
        request = self.context.get("request")
        if ticket.user.pk != request.user.pk:
            raise serializers.ValidationError("Ticket does not belong to user")
        if Result.objects.filter(ticket=ticket).exists():
            raise serializers.ValidationError("Result already exists for this ticket")
        # TODO: validate ticket current status?
        return ticket
