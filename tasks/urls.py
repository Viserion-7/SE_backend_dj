from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'subtasks', views.SubTaskViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'reminders', views.ReminderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    # Additional reminder-specific endpoints are handled by the TaskViewSet actions:
    # POST /api/tasks/check_reminders/
    # GET /api/tasks/reminder_status/
]
