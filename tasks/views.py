from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task, SubTask, Category, Reminder
from .serializers import TaskSerializer, SubTaskSerializer, CategorySerializer, ReminderSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(task__user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response(
            {'error': 'Please provide username, email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'username': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'email': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

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
            'email': user.email
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
