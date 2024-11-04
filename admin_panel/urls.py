# admin_panel/urls.py

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    WeekDayViewSet, CourseViewSet, TariffViewSet, TeacherViewSet,
    GroupViewSet, StudentViewSet, EvaluationViewSet, PaymentViewSet,
    AttendanceViewSet, GetAllStudentsViewSet, BlogsViewSet
)

router = DefaultRouter()
router.register(r'weekdays', WeekDayViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'tariffs', TariffViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'all_students', GetAllStudentsViewSet, basename='all_students')
router.register(r'blogs', BlogsViewSet, basename='blogs')

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('guruhlar/', views.groups, name='groups'),
    path('guruhlar/add/', views.add_group, name='add_group'),
    path('guruhlar/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('guruhlar/delete/<int:group_id>/', views.delete_group, name='delete_group'),

    path('kurslar/', views.courses, name='courses'),
    path('kurslar/add/', views.add_course, name='add_course'),
    path('kurslar/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('kurslar/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    
    path('ustozlar/', views.teachers, name='teachers'),
    path('ustozlar/add/', views.add_teacher, name='add_teacher'),
    path('ustozlar/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('ustozlar/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),

    path('tariflar/', views.tariffs, name='tariffs'),
    path('tariflar/add/', views.add_tariff, name='add_tariff'),
    path('tariflar/edit/<int:tariff_id>/', views.edit_tariff, name='edit_tariff'),
    path('tariflar/delete/<int:tariff_id>/', views.delete_tariff, name='delete_tariff'),

    path('tolovlar/', views.payments, name='payments'),
    path('tolovlar/add/', views.add_payment, name='add_payment'),
    path('tolovlar/edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('tolovlar/delete/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('tolovlar/get_students/<int:group_id>/', views.get_students_for_payment, name='get_students_for_payment'),

    path('talabalar/', views.students, name='students'),
    path('talabalar/add/', views.add_student, name='add_student'),
    path('talabalar/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('talabalar/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    path('davomatlar/', views.attendances, name='attendances'),
    path('davomatlar/add/', views.add_attendance, name='add_attendance'),
    path('davomatlar/edit/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    path('davomatlar/delete/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('davomatlar/get_students/<int:group_id>/', views.get_students, name='get_students'),

    path('baholash/', views.evaluations, name='evaluations'),
    path('baholash/add/', views.add_evaluation, name='add_evaluation'),
    path('baholash/edit/<int:evaluation_id>/', views.edit_evaluation, name='edit_evaluation'),
    path('baholash/delete/<int:evaluation_id>/', views.delete_evaluation, name='delete_evaluation'),
    path('baholash/get_students/<int:group_id>/', views.get_students_evaluation, name='get_students_evaluation'),

    path('permission-denied/', views.permission_denied, name='permission_denied'),

    path('api/', include(router.urls)),
]