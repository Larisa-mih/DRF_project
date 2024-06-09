from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("create", UserCreateAPIView.as_view(), name="user_create"),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("detail/<int:pk>", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>", UserUpdateAPIView.as_view(), name="user_update"),
    path("delete/<int:pk>", UserDestroyAPIView.as_view(), name="user_delete"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path(
        "token",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
