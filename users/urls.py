from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PaymentViewSet, UserProfileViewSet, SubscriptionAPIView

router = DefaultRouter()

router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls + [
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]