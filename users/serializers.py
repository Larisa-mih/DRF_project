from rest_framework import serializers

from users.models import Payment, User
from users.services import retrieve_strip_session


class PaymentSerializer(serializers.ModelSerializer):
    """Класс сериализатор платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentStatusSerializer(serializers.ModelSerializer):
    """Класс сериализатор статуса платежа"""
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        exclude = ['payment_link', ]

    @staticmethod
    def get_payment_status(instance):
        return retrieve_strip_session(instance.payment_id)


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатор пользователя"""
    payment = PaymentSerializer(source="payment_set", many=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "phone", "city", "payment"]


class CreateUserSerializer(serializers.ModelSerializer):
    """Класс сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"], password=validated_data["password"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializerPerm(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "city", "email"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Класс сериализатор информации пользователя с платежами"""
    payments_list = PaymentSerializer(source='payments_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'is_superuser', 'is_staff', 'is_active',
                  'payments_list']
