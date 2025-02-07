from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"

    def validate_ticket(self, ticket):
        request = self.context.get("request")
        if ticket.user.id != request.user.id:
            raise serializers.ValidationError("Ticket does not belong to user")
        if Result.objects.filter(ticket=ticket).exists():
            raise serializers.ValidationError("Result already exists for this ticket")
        # TODO: validate ticket current status?
        return ticket
