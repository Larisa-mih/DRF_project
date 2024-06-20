from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsAuth
from users.serializers import (
    CreateUserSerializer,
    PaymentSerializer,
    UserSerializer,
    UserSerializerPerm, PaymentStatusSerializer,
)
from users.services import create_strip_product, create_strip_price, create_strip_session, retrieve_strip_session


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания пользователя"""
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Эндпоинт просмотра списка пользователей"""
    serializer_class = UserSerializerPerm
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAuth]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAuth]


class PaymentListAPIView(generics.ListAPIView):
    """Эндпоинт просмотра списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course_paid", "subject_paid", "payment_method")
    ordering_fields = ("payment_date",)
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания платежа"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_strip_product(payment)
        price_id = create_strip_price(product_id, payment)
        payment.payment_id, payment.payment_link = create_strip_session(price_id)
        payment.payment_status = retrieve_strip_session(payment.payment_id)
        payment.save()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра статуса платежа"""
    serializer_class = PaymentStatusSerializer
    queryset = Payment.objects.all()
