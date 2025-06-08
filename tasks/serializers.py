from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, SubTask, Category, Reminder

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'minutes', 'is_completed', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 
            'due_date', 'is_completed', 'category', 
            'created_at', 'updated_at'
        ]

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'task', 'remind_at', 'sent']
