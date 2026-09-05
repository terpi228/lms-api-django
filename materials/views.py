from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from .permissions import IsModer, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ~IsModer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner(), ~IsModer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModer() | IsOwner()]
        else:  # list, retrieve
            return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ~IsModer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner(), ~IsModer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModer() | IsOwner()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)