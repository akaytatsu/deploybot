from django.contrib import admin
from apps.rundeck.models import Jobs, JobStatus


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    fields = ['id', 'href', 'enabled', 'permalink', 'name', 'project', 'description', 'use_chatbot']
    readonly_fields = ['id', 'href', 'enabled', 'permalink', 'name', 'project', 'description']
    list_display = [ 'name', 'project', 'description', 'enabled', 'use_chatbot']
    search_fields = ['name', "description"]
    list_filter = ["use_chatbot", "enabled", ]


@admin.register(JobStatus)
class JobStatusAdmin(admin.ModelAdmin):
    pass