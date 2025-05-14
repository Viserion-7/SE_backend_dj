from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Task, SubTask, Category, Reminder
from .serializers import TaskSerializer, SubTaskSerializer, CategorySerializer, ReminderSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        # Return tasks only for the authenticated user
        return self.queryset.filter(user=self.request.user)


class SubTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing subtasks.
    """
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return subtasks only for tasks owned by the authenticated user
        return self.queryset.filter(task__user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all categories (can be global or user-specific if needed)
        return self.queryset


class ReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reminders.
    """
    serializer_class = ReminderSerializer
    queryset = Reminder.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return reminders only for tasks owned by the authenticated user
        return self.queryset.filter(task__user=self.request.user)