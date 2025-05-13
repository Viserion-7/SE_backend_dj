from django.contrib import admin
from .models import Task, SubTask, Category, Reminder


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'is_completed', 'get_categories', 'created_at', 'updated_at')
    list_filter = ('priority', 'is_completed', 'due_date', 'categories')
    search_fields = ('title', 'description', 'categories__name')
    ordering = ('due_date',)
    autocomplete_fields = ('categories',)
    date_hierarchy = 'due_date'

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = "Categories"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'is_completed', 'due_date')
    list_filter = ('is_completed', 'due_date')
    search_fields = ('title', 'task__title')
    ordering = ('due_date',)
    date_hierarchy = 'due_date'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'remind_at', 'sent')
    list_filter = ('sent', 'remind_at')
    search_fields = ('task__title',)
    ordering = ('remind_at',)
    date_hierarchy = 'remind_at'