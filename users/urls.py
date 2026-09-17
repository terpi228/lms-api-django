from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls