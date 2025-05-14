from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TaskViewSet, SubTaskViewSet, CategoryViewSet, ReminderViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'reminders', ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]