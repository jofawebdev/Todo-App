from django.contrib import admin
from .models import Task, Profile

# Register Task model with the admin site 
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'priority', 'completed')
    list_filter = ('priority', 'completed')
    search_fields = ('title', 'description')
    ordering = ('due_date',)


admin.site.register(Profile)