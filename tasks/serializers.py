from rest_framework import serializers
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
    categories = CategorySerializer(many=True)  # Allow category details

    class Meta:
        model = Task
        fields = [
            'id', 'user', 'title', 'description', 'priority', 'due_date', 
            'is_completed', 'categories', 'reminders', 'subtasks', 
            'created_at', 'updated_at'
        ]