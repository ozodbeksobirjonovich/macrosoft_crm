# admin_panel/serializers.py

from rest_framework import serializers
from .models import (
    WeekDay, Course, Tariff, Teacher, Group,
    Student, Evaluation, Payment, Attendance,
    Blogs
)
from django.db.models import Sum

class WeekDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekDay
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    tariff = TariffSerializer(read_only=True)
    days_of_week = WeekDaySerializer(many=True, read_only=True)
    days_of_week_ids = serializers.PrimaryKeyRelatedField(
        queryset=WeekDay.objects.all(),
        many=True,
        write_only=True,
        source='days_of_week'
    )

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'teacher', 'course', 'start_date', 'end_date',
            'lesson_start_time', 'lesson_end_time', 'tariff',
            'days_of_week', 'days_of_week_ids', 'hours', 'duration'
        ]

class StudentSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        source='groups'
    )

    class Meta:
        model = Student
        fields = [
            'id', 'fullname', 'image', 'groups', 'group_ids',
            'phone1', 'phone2', 'phone3'
        ]

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

    def validate_score(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError("Baho 0 dan 10 gacha bo'lishi kerak.")
        return value

    def validate(self, attrs):
        # Ensure uniqueness of student and group
        if Evaluation.objects.filter(student=attrs['student'], group=attrs['group']).exists():
            raise serializers.ValidationError("Bu talabaga bu guruhda baho allaqachon mavjud.")
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def validate(self, attrs):
        # Ensure uniqueness of student and date
        if Attendance.objects.filter(student=attrs['student'], date=attrs['date']).exists():
            raise serializers.ValidationError("Bu talabaga ushbu sanada davomat allaqachon mavjud.")
        return attrs

class TeacherDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['fullname', 'image']

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']

class GroupDetailSerializer(serializers.ModelSerializer):
    teacher = TeacherDetailSerializer(read_only=True)
    course = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'teacher', 'course']

class StudentNoPhoneSerializer(serializers.ModelSerializer):
    groups = GroupDetailSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'fullname', 'image', 'score', 'groups'
        ]

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_score(self, obj):
        total_score = Evaluation.objects.filter(student=obj).aggregate(total=Sum('score'))['total']
        return total_score or 0
    
class BlogsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blogs
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None