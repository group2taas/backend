from django.contrib import admin
from .models import Interview, Answer, Question

# Register your models here.
admin.site.register(Question)
admin.site.register(Interview)
admin.site.register(Answer)
