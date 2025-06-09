from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'subtasks', views.SubTaskViewSet, basename='subtask')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('tasks/<int:pk>/subtasks/', views.TaskViewSet.as_view({'get': 'subtasks'}), name='task-subtasks'),
    path('subtasks/<int:pk>/complete/', views.SubTaskViewSet.as_view({'put': 'complete'}), name='subtask-complete'),
]
