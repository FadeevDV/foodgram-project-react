from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConfirmationCodeView, UserLoginView, UserViewSet

v1_patterns = (
    [
        path('email', ConfirmationCodeView.as_view()),
        path('token', UserLoginView.as_view()),
    ]
)

v1_router = DefaultRouter()

v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('auth/', include(v1_patterns)),
    path('', include(v1_router.urls)),
]
