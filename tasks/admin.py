from django.contrib import admin
from .models import Task, SubTask, Category, Reminder

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'is_completed', 'category')
    list_filter = ('is_completed', 'priority', 'category')
    search_fields = ('title', 'description')
    ordering = ('-due_date',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'minutes', 'is_completed', 'created_at')
    list_filter = ('is_completed',)
    search_fields = ('title', 'task')
    ordering = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'remind_at', 'sent')
    list_filter = ('sent',)
    ordering = ('remind_at',)
