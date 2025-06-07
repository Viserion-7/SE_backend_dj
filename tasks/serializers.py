from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category, Reminder

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'task', 'remind_at', 'sent']

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'is_completed', 'due_date']

class TaskSerializer(serializers.ModelSerializer):
    reminders = ReminderSerializer(many=True, read_only=True)  # Nested reminders
    subtasks = SubTaskSerializer(many=True, read_only=True)  # Nested subtasks
    category_name = serializers.CharField(source='category.name', read_only=True)  # Add category name
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make user read-only
    due_date = serializers.DateTimeField(
        required=True,
        error_messages={
            'required': 'Due date is required',
            'invalid': 'Invalid date format. Please use YYYY-MM-DD format'
        }
    )

    def validate_due_date(self, value):
        """
        Validate the due date:
        1. Convert to timezone-aware datetime if it isn't already
        2. Ensure it's not in the past
        """
        if timezone.is_naive(value):
            value = timezone.make_aware(value)
        
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    class Meta:
        model = Task
        fields = [
            'id', 'user', 'title', 'description', 'priority', 'due_date', 
            'is_completed', 'category', 'category_name', 'reminders', 'subtasks', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
