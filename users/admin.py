from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import UserProfile
from tickets.models import Ticket
from loguru import logger

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name')
    list_filter = ('company_name', 'is_staff', 'is_active')  
    search_fields = ('name', 'email', 'company_name', 'uid')
    readonly_fields = ('uid', 'ticket_count', 'user_tickets', 'user_actions')
    fieldsets = (
        ('Personal Information', {
            'fields': ('uid', 'name', 'email', 'phone')
        }),
        ('Company Information', {
            'fields': ('company_name',)
        }),
        ('Account Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Security Testing', {
            'fields': ('ticket_count', 'user_tickets')
        })
    )
    
    def get_queryset(self, request):
        try:
            queryset = super().get_queryset(request)
            queryset = queryset.annotate(
                _ticket_count=Count('ticket', distinct=True),
            )
            return queryset
        except Exception as e:
            logger.error(f"Error in get_queryset: {e}")
            return super().get_queryset(request)
    
    def ticket_count(self, obj):
        try:
            if hasattr(obj, '_ticket_count'):
                count = obj._ticket_count
            else:
                count = Ticket.objects.filter(user=obj).count()
            
            url = reverse('admin:tickets_ticket_changelist') + f'?user__uid={obj.uid}'
            if count > 0:
                return format_html('<a href="{}">{} tickets</a>', url, count)
            return '0 tickets'
        except Exception as e:
            logger.error(f"Error in ticket_count: {e}")
            return '0 tickets'
    ticket_count.short_description = 'Tickets'
    ticket_count.admin_order_field = '_ticket_count'
    
    def user_tickets(self, obj):
        try:
            tickets = Ticket.objects.filter(user=obj).order_by('-created_at')
            if not tickets:
                return 'No tickets'
                
            result = []
            for ticket in tickets:
                url = reverse('admin:tickets_ticket_change', args=[ticket.id])
                status_colors = {
                    'new': 'blue',
                    'testing': 'orange',
                    'completed': 'green',
                }
                color = status_colors.get(ticket.status, 'gray')
                status_badge = f'<span style="background-color:{color}; color:white; padding:2px 5px; border-radius:3px; font-size:0.8em;">{ticket.status.upper()}</span>'
                result.append(f'<div style="margin-bottom:5px;"><a href="{url}">{ticket.title}</a> {status_badge} ({ticket.created_at.strftime("%Y-%m-%d")})</div>')
                
            return format_html(''.join(result))
        except Exception as e:
            logger.error(f"Error in user_tickets: {e}")
            return 'Error loading tickets'
    user_tickets.short_description = 'Recent Tickets'
    
    def user_actions(self, obj):
        try:
            view_tickets = reverse('admin:tickets_ticket_changelist') + f'?user__uid={obj.uid}'
            return format_html(
                '<a class="button" href="{}">View Tickets</a>',
                view_tickets
            )
        except Exception as e:
            logger.error(f"Error in user_actions: {e}")
            return "Actions unavailable"
    user_actions.short_description = 'Actions'