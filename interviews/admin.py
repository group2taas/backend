from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Interview, Answer, Question
from loguru import logger

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'question_type', 'is_required', 'answer_count')
    list_filter = ('type', 'is_required')
    search_fields = ('text',)
    
    def text_preview(self, obj):
        max_length = 50
        if len(obj.text) > max_length:
            return obj.text[:max_length] + '...'
        return obj.text
    text_preview.short_description = 'Question'
    
    def question_type(self, obj):
        type_colors = {
            'text': '#6c757d',
            'short-text': '#007bff',
            'radio': '#28a745',
            'select': '#17a2b8',
            'select-multiple': '#fd7e14',
            'integer': '#dc3545',
            'float': '#6610f2',
            'date': '#20c997',
        }
        color = type_colors.get(obj.type, '#6c757d')
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color, obj.get_type_display()
        )
    question_type.short_description = 'Type'
    
    def answer_count(self, obj):
        count = Answer.objects.filter(question=obj).count()
        return count
    answer_count.short_description = 'Answers'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'answer_preview', 'interview_link', 'updated_at')
    list_filter = ('updated_at', 'question__type')
    search_fields = ('body', 'question__text')
    raw_id_fields = ('question', 'interview')
    
    def question_text(self, obj):
        url = reverse('admin:interviews_question_change', args=[obj.question.id])
        return format_html('<a href="{}">{}</a>', url, obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text)
    question_text.short_description = 'Question'
    
    def answer_preview(self, obj):
        if not obj.body:
            return 'No answer'
        max_length = 50
        preview = obj.body[:max_length] + '...' if len(obj.body) > max_length else obj.body
        return format_html('<span title="{}">{}</span>', obj.body, preview)
    answer_preview.short_description = 'Answer'
    
    def interview_link(self, obj):
        url = reverse('admin:interviews_interview_change', args=[obj.interview.id])
        return format_html('<a href="{}">{}</a>', url, f'Interview #{obj.interview.id}')
    interview_link.short_description = 'Interview'

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_link', 'created_at', 'answer_count', 'user_info')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('ticket__title',)
    readonly_fields = ('created_at', 'updated_at', 'answer_count', 'answer_details', 'ticket_link', 'user_info', 'results_link')
    
    def get_queryset(self, request):
        try:
            queryset = super().get_queryset(request)
            return queryset
        except Exception as e:
            logger.error(f"Error in interview admin get_queryset: {e}")
            return super().get_queryset(request)
    
    def answer_count(self, obj):
        try:
            return obj.answers.count()
        except Exception as e:
            logger.error(f"Error in answer_count: {e}")
            return 0
    answer_count.short_description = 'Answers'
    
    def ticket_link(self, obj):
        url = reverse('admin:tickets_ticket_change', args=[obj.ticket.id])
        return format_html('<a href="{}">{}</a>', url, obj.ticket.title)
    ticket_link.short_description = 'Ticket'
    
    def user_info(self, obj):
        try:
            if not hasattr(obj, 'ticket') or not obj.ticket:
                return "No ticket associated"
            
            if not hasattr(obj.ticket, 'user') or not obj.ticket.user:
                return "No user associated"
                
            user = obj.ticket.user
            url = reverse('admin:users_userprofile_change', args=[str(user.uid)])
            return format_html('<a href="{}">{}</a> ({})', url, user.name, user.company_name)
        except Exception as e:
            logger.error(f"Error in user_info admin method: {e}")
            return "User information unavailable"
    user_info.short_description = 'User'
    
    def answer_details(self, obj):
        try:
            answers = obj.answers.select_related('question').all()
            if not answers:
                return 'No answers recorded'
            
            result = ['<table style="width:100%; border-collapse:collapse;">',
                      '<tr><th style="text-align:left; padding:8px; border-bottom:1px solid #ddd;">Question</th>' +
                      '<th style="text-align:left; padding:8px; border-bottom:1px solid #ddd;">Answer</th></tr>']
            
            for answer in answers:
                question = answer.question.text if answer.question else 'Unknown question'
                answer_text = answer.body or 'No answer'
                result.append(f'<tr><td style="padding:8px; border-bottom:1px solid #ddd;">{question}</td>' +
                              f'<td style="padding:8px; border-bottom:1px solid #ddd;">{answer_text}</td></tr>')
            
            result.append('</table>')
            return format_html(''.join(result))
        except Exception:
            return 'Unable to display answers'
    answer_details.short_description = 'Answers Detail'
    
    def results_link(self, obj):
        try:
            from results.models import Result
            results = Result.objects.filter(ticket=obj.ticket)
            
            if not results:
                return 'No results available'
            
            links = []
            for result in results:
                url = reverse('admin:results_result_change', args=[result.id])
                links.append(f'<a href="{url}">{result.title or f"Result #{result.id}"}</a>')
                
            return format_html('<br>'.join(links))
        except Exception:
            return 'Results unavailable'
    results_link.short_description = 'Related Results'
