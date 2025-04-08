from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Ticket
from results.models import Result
from interviews.models import Interview

# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status_badge', 'created_at', 'user', 'show_details', 'related_links')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('title', 'details')
    readonly_fields = ('created_at', 'status_badge', 'show_details', 'related_links')
    fieldsets = (
        (None, {
            'fields': ('title', 'status_badge', 'user')
        }),
        ('Timing', {
            'fields': ('created_at',),
        }),
        ('Additional Information', {
            'fields': ('details', 'related_links'),
            'classes': ('collapse',),
        }),
    )
    
    def status_badge(self, obj):
        status_colors = {
            'new': 'blue',
            'testing': 'orange',
            'completed': 'green',
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; border-radius:5px;">{}</span>',
            color, obj.status.upper()
        )
    status_badge.short_description = 'Status'
    
    def show_details(self, obj):
        if obj.details:
            return format_html(
                '<span title="{}">View Details</span>',
                str(obj.details)
            )
        return 'No details'
    show_details.short_description = 'Details'
    
    def related_links(self, obj):
        interviews = Interview.objects.filter(ticket=obj)
        results = Result.objects.filter(ticket=obj)
        
        links = []
        
        for interview in interviews:
            url = reverse('admin:interviews_interview_change', args=[interview.id])
            links.append(f'<a href="{url}">Interview #{interview.id}</a>')
        
        for result in results:
            url = reverse('admin:results_result_change', args=[result.id])
            links.append(f'<a href="{url}">Result: {result.title or f"#{result.id}"}</a>')
        
        if links:
            return format_html('<br>'.join(links))
        return 'No related records'