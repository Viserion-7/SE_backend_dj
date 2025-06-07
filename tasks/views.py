from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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

    def perform_create(self, serializer):
        # Automatically set the authenticated user
        serializer.save(user=self.request.user)


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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Validate required fields
    if not all([username, email, password]):
        return Response(
            {'error': 'Please provide username, email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'username': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if email exists
    if User.objects.filter(email=email).exists():
        return Response(
            {'email': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user with username and password.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': password  # Include password for Basic Auth
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
