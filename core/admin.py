from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from tickets.models import Ticket
from users.models import UserProfile
from results.models import Result
from interviews.models import Interview, Answer

# Register custom admin view
@staff_member_required
def admin_dashboard(request):
    ticket_status = (
        Ticket.objects.values('status')
        .annotate(count=Count('status'))
        .order_by('status')
    )
    
    users_with_tickets = (
        UserProfile.objects.annotate(
            ticket_count=Count('ticket')
        )
    )
    
    results_with_alerts = Result.objects.all()
    
    interview_count = Interview.objects.count()
    answers_count = Answer.objects.count()
    
    # Aggregate security alert data
    high_alerts = 0
    medium_alerts = 0
    low_alerts = 0
    info_alerts = 0
    
    for result in results_with_alerts:
        alert_counts = result.get_alert_counts()
        high_alerts += alert_counts.get('High', 0)
        medium_alerts += alert_counts.get('Medium', 0)
        low_alerts += alert_counts.get('Low', 0)
        info_alerts += alert_counts.get('Informational', 0)
    
    context = {
        'ticket_status': ticket_status,
        'users_with_tickets': users_with_tickets,
        'total_users': UserProfile.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'results_count': Result.objects.count(),
        'interview_count': interview_count,
        'answers_count': answers_count,
        'high_alerts': high_alerts,
        'medium_alerts': medium_alerts,
        'low_alerts': low_alerts,
        'info_alerts': info_alerts,
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
        'title': 'Security Testing Dashboard',
    }
    
    return TemplateResponse(request, 'admin/dashboard.html', context)

admin.site.site_header = 'Security Testing Admin'
admin.site.site_title = 'Security Testing Admin Portal'
admin.site.index_title = 'Security Testing Dashboard'