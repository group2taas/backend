from django.contrib import admin
from .models import Result

# Register your models here.

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('num_tests', 'logs', 'security_alerts')
    readonly_fields = ('created_at',)