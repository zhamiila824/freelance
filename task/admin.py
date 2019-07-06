from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'title', 'customer', 'description', 'price', 'done', 'executor')


admin.site.register(Task, TaskAdmin)
