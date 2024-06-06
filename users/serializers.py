from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'is_staff']


class UserDetailSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'is_staff', 'payment']
