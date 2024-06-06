from rest_framework import generics

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserDetailSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course_paid", "subject_paid", "payment_method")
    ordering_fields = ("payment_date",)
