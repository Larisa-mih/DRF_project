from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDestroyAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("create", UserCreateAPIView.as_view(), name="user_create"),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("detail/<int:pk>", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>", UserUpdateAPIView.as_view(), name="user_update"),
    path("delete/<int:pk>", UserDestroyAPIView.as_view(), name="user_delete"),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
