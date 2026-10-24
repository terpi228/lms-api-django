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
from .services import create_stripe_checkout
from stripe import StripeError
from rest_framework.exceptions import APIException


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAuthenticated()]

class StripeServiceError(APIException):
    status_code = 502
    default_detail = "Не удалось создать оплату через Stripe."
    default_code = "stripe_error"
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

    def perform_create(self, serializer):
        data = serializer.validated_data
        stripe_data = {}

        if data["payment_method"] == "stripe":
            course = data.get("paid_course") or data.get("paid_lesson")

            try:
                stripe_data = create_stripe_checkout(
                    course,
                    data["amount"],
                )
            except StripeError as exc:
                raise StripeServiceError() from exc

        serializer.save(**stripe_data)

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