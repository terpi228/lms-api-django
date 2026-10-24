from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.models import Course
from .models import Payment, User, Subscription
from .serializers import (
    CustomTokenObtainPairSerializer,
    PaymentSerializer,
    UserSerializer,
    SubscriptionSerializer,
    SubscriptionResponseSerializer,
    ErrorResponseSerializer,
)
from drf_spectacular.utils import extend_schema


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAuthenticated()]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SubscriptionSerializer,
        responses={200: SubscriptionResponseSerializer,
                   401: ErrorResponseSerializer,
                   404: ErrorResponseSerializer},
    )

    def post(self, request):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)    

        subscriptions  = Subscription.objects.filter(
            user=user, 
            course=course
            )
    
        if subscriptions.exists():
            subscriptions.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})