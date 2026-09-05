from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]