from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, Lesson
from .paginators import MaterialsPagination
from .permissions import IsModer, IsNotModer, IsOwner
from .serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination
    ordering = ['id']

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
            return [IsAuthenticated(), (IsModer | IsOwner)()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='moderators').exists():
            return Course.objects.order_by('id')
        if user.is_authenticated:
            return Course.objects.filter(owner=user).order_by('id')
        return Course.objects.order_by('id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPagination
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNotModer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwner(), IsNotModer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), (IsModer | IsOwner)()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='moderators').exists():
            return Lesson.objects.order_by('id')
        if user.is_authenticated:
            return Lesson.objects.filter(owner=user).order_by('id')
        return Lesson.objects.order_by('id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)