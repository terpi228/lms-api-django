from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, Lesson
from .permissions import IsModer, IsNotModer, IsOwner
from .serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNotModer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner(), IsNotModer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModer() | IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        if user.is_authenticated:
            return Course.objects.filter(owner=user)
        return Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNotModer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner(), IsNotModer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModer() | IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        if user.is_authenticated:
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)