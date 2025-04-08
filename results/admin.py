from django.contrib import admin
from django.utils.html import format_html
from .models import Result

# Register your models here.

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'ticket', 'created_at', 'progress_bar', 'alert_summary', 'view_pdf')
    list_filter = ('created_at', 'ticket')
    search_fields = ('title', 'ticket__title')
    readonly_fields = ('created_at', 'progress_bar', 'alert_summary', 'view_pdf')
    
    def progress_bar(self, obj):
        percent = 0
        if obj.num_tests > 0:
            percent = int(obj.progress / obj.num_tests * 100) if obj.num_tests > 0 else 0
        
        color = 'green' if percent == 100 else 'orange'
        return format_html(
            '<div style="width:100%%; background-color:#ddd; border-radius:3px;">' +
            '<div style="width:{}%%; background-color:{}; height:20px; border-radius:3px;">' +
            '<div style="padding-left:5px; color:white;">{}/{} ({}%)</div>' +
            '</div></div>',
            percent, color, obj.progress, obj.num_tests, percent
        )
    progress_bar.short_description = 'Progress'
    
    def alert_summary(self, obj):
        alert_counts = obj.get_alert_counts()
        high = alert_counts.get('High', 0)
        medium = alert_counts.get('Medium', 0)
        low = alert_counts.get('Low', 0)
        info = alert_counts.get('Informational', 0)
        
        return format_html(
            '<span style="color:red; font-weight:bold;">{} High</span>, ' +
            '<span style="color:orange; font-weight:bold;">{} Medium</span>, ' +
            '<span style="color:blue;">{} Low</span>, ' +
            '<span style="color:gray;">{} Info</span>',
            high, medium, low, info
        )
    alert_summary.short_description = 'Security Alerts'
    
    def view_pdf(self, obj):
        if obj.pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf.url)
        return 'No PDF'
    view_pdf.short_description = 'Report'