from rest_framework import serializers

from materials.models import Course, Subject


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    class Meta:
        model = Course
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""
    class Meta:
        model = Subject
        fields = '__all__'
