from django.contrib import admin
from .models import Ticket

# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'user')
    search_fields = ('title', 'details')
    readonly_fields = ('created_at',)