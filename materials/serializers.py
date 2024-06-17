from rest_framework import serializers

from materials.models import Course, Subject, Subscription
from materials.validators import LinkValidator


class SubjectSerializer(serializers.ModelSerializer):
    """Класс сериализатор урока"""
    validators = [LinkValidator(field="link")]

    class Meta:
        model = Subject
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Класс сериализатор курса"""
    subject_count = serializers.SerializerMethodField()
    subject = SubjectSerializer(source="subject_set", many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_subject_count(course):
        return Subject.objects.filter(course=course).count()

    def get_subscription(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.subscription_set.filter(user=user).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """""Класс сериализатор подписки"""""
    class Meta:
        model = Subscription
        fields = "__all__"
