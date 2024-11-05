# admin_panel/views.py!

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Attendance, Group, Student
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from .forms import GroupForm, CourseForm, TariffForm, TeacherForm, PaymentForm

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentNoPhoneSerializer
from django.shortcuts import render, redirect
from .models import (
    WeekDay, Course, Tariff, Teacher, Group,
    Student, Evaluation, Payment, Attendance,
    Blogs
)

from .serializers import (
    WeekDaySerializer, CourseSerializer, TariffSerializer,
    TeacherSerializer, GroupSerializer, StudentSerializer,
    EvaluationSerializer, PaymentSerializer, AttendanceSerializer,
    BlogsSerializer
)


def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

##############################################################################

##############################################################################

def dashboard(request):
    return render(request, "dashboard.html")

# PERMISSION START
##########################################################################################################
def permission_denied_view(request, exception=None):
    return render(request, 'permission_denied.html', status=403)

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('admin_panel:permission_denied')
    return _wrapped_view

@login_required
def permission_denied(request):
    return render(request, 'permission_denied.html')
##########################################################################################################
# PERMISSION END


# GROUPS START
##########################################################################################################
@login_required
def groups(request):
    groups = Group.objects.all()
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    tariffs = Tariff.objects.all()
    weekdays = WeekDay.objects.all()
    time_choices = [choice[0] for choice in [("08:00", "08:00"), ("08:30", "08:30"), ("09:00", "09:00"), ("09:30", "09:30"),
                 ("10:00", "10:00"), ("10:30", "10:30"), ("11:00", "11:00"), ("11:30", "11:30"),
                 ("12:00", "12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"),
                 ("14:00", "14:00"), ("14:30", "14:30"), ("15:00", "15:00"), ("15:30", "15:30"),
                 ("16:00", "16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"),
                 ("18:00", "18:00"), ("18:30", "18:30"), ("19:00", "19:00"), ("19:30", "19:30"),
                 ("20:00", "20:00")]]
    
    context = {
        'groups': groups,
        'teachers': teachers,
        'courses': courses,
        'tariffs': tariffs,
        'weekdays': weekdays,
        'time_choices': time_choices,
    }
    
    return render(request, "guruhlar.html", context)

@superuser_required
@login_required
@require_POST
def add_group(request):
    form = GroupForm(request.POST)
    if form.is_valid():
        group = form.save(commit=False)  # Obtain Group instance without saving to DB
        group.save()                      # Save Group instance to DB
        form.save_m2m()                   # Save ManyToMany relationships
        messages.success(request, "Guruh muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:groups')

@superuser_required
@login_required
@require_POST
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        messages.success(request, "Guruh muvaffaqiyatli yangilandi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:groups')

@superuser_required
@login_required
@require_POST
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, "Guruh muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:groups')
##########################################################################################################
# GROUPS END

# COURSES START
##########################################################################################################
@login_required
def courses(request):
    courses = Course.objects.all()
    return render(request, "kurslar.html", {'courses': courses})

@login_required
@require_POST
def add_course(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Kurs muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:courses')

@login_required
@require_POST
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST, instance=course)
    if form.is_valid():
        form.save()
        messages.success(request, "Kurs muvaffaqiyatli yangilandi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:courses')

@login_required
@require_POST
def delete_course(request, course_id):
    """
    Handle the deletion of a course.
    """
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Kurs muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:courses')
##########################################################################################################
# COURSES END

# TEACHERS START
##########################################################################################################
@login_required
def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, "ustozlar.html", {'teachers': teachers})

@superuser_required
@login_required
@require_POST
def add_teacher(request):
    form = TeacherForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Ustoz muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:teachers')

@superuser_required
@login_required
@require_POST
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    form = TeacherForm(request.POST, request.FILES, instance=teacher)
    if form.is_valid():
        form.save()
        messages.success(request, "Ustoz muvaffaqiyatli yangilandi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:teachers')

@superuser_required
@login_required
@require_POST
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    messages.success(request, "Ustoz muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:teachers')
##########################################################################################################
# TEACHERS END

# TARIFF START
##########################################################################################################
@login_required
def tariffs(request):
    tariffs = Tariff.objects.all()
    return render(request, "tariflar.html", {'tariffs': tariffs})

@login_required
@require_POST
def add_tariff(request):
    form = TariffForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Tarif muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:tariffs')

@login_required
@require_POST
def edit_tariff(request, tariff_id):
    tariff = get_object_or_404(Tariff, id=tariff_id)
    form = TariffForm(request.POST, instance=tariff)
    if form.is_valid():
        form.save()
        messages.success(request, "Tarif muvaffaqiyatli yangilandi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:tariffs')

@login_required
@require_POST
def delete_tariff(request, tariff_id):
    tariff = get_object_or_404(Tariff, id=tariff_id)
    tariff.delete()
    messages.success(request, "Tarif muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:tariffs')
##########################################################################################################
# TARIFF END

# PAYMENTS START
##########################################################################################################

@login_required
def payments(request):
    payments = Payment.objects.select_related('student', 'group').all()
    students = Student.objects.all()
    groups = Group.objects.all()
    return render(request, "tolovlar.html", {'payments': payments, 'students': students, 'groups': groups})

@superuser_required
@login_required
@require_POST
def add_payment(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "To'lov muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:payments')

@superuser_required
@login_required
@require_POST
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    form = PaymentForm(request.POST, instance=payment)
    if form.is_valid():
        form.save()
        messages.success(request, "To'lov muvaffaqiyatli yangilandi.")
    else:
        messages.error(request, "Ma'lumotlarni to'g'ri kiriting.")
    return redirect('admin_panel:payments')

@superuser_required
@login_required
@require_POST
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    messages.success(request, "To'lov muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:payments')

@login_required
@require_GET
def get_students_for_payment(request, group_id):
    """
    Fetch students belonging to a specific group via AJAX for Payment.
    Returns JSON response with student IDs and fullnames.
    """
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    serialized_students = [
        {'id': student.id, 'fullname': student.fullname}
        for student in students
    ]
    return JsonResponse({'students': serialized_students})
##########################################################################################################
# PAYMENTS END

# STUDENTS START
##########################################################################################################
@login_required
def students(request):
    students = Student.objects.all()
    all_groups = Group.objects.all()
    return render(request, "talabalar.html", {'students': students, 'all_groups': all_groups})

@login_required
@require_POST
def add_student(request):
    fullname = request.POST.get('fullname')
    image = request.FILES.get('image')
    groups = request.POST.getlist('groups')
    phone1 = request.POST.get('phone1')
    phone2 = request.POST.get('phone2')
    phone3 = request.POST.get('phone3')

    if not fullname or not phone1:
        messages.error(request, "To'liq ism va Telefon 1 maydonlari talab qilinadi.")
        return redirect('admin_panel:students')

    student = Student.objects.create(
        fullname=fullname,
        image=image,
        phone1=phone1,
        phone2=phone2,
        phone3=phone3,
    )
    if groups:
        student.groups.set(groups)
    student.save()

    messages.success(request, "Talaba muvaffaqiyatli qo'shildi.")
    return redirect('admin_panel:students')

@login_required
@require_POST
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    fullname = request.POST.get('fullname')
    image = request.FILES.get('image')
    groups = request.POST.getlist('groups')
    phone1 = request.POST.get('phone1')
    phone2 = request.POST.get('phone2')
    phone3 = request.POST.get('phone3')

    if not fullname or not phone1:
        messages.error(request, "To'liq ism va Telefon 1 maydonlari talab qilinadi.")
        return redirect('admin_panel:students')

    student.fullname = fullname
    if image:
        student.image = image
    student.phone1 = phone1
    student.phone2 = phone2
    student.phone3 = phone3
    if groups:
        student.groups.set(groups)
    else:
        student.groups.clear()
    student.save()

    messages.success(request, "Talaba muvaffaqiyatli yangilandi.")
    return redirect('admin_panel:students')

@login_required
@require_POST
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Talaba muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:students')
##########################################################################################################
# STUDENTS END

# ATTENDANCE START
##########################################################################################################
@login_required
def attendances(request):
    attendances = Attendance.objects.select_related('student', 'group').all()
    groups = Group.objects.all()
    return render(request, "davomatlar.html", {'attendances': attendances, 'groups': groups})

@login_required
@require_POST
def add_attendance(request):
    group_id = request.POST.get('group')
    date = request.POST.get('date')
    present_students = request.POST.getlist('present_students')  # List of student IDs who are present

    print(group_id, date, present_students)

    if not group_id or not date:
        messages.error(request, "Guruh va sana maydonlari talab qilinadi.")
        return redirect('admin_panel:attendances')

    group = get_object_or_404(Group, id=group_id)
    group_students = Student.objects.filter(groups=group)

    if group_students:
        for student in group_students:
            present = str(student.id) in present_students
            attendance_exists = Attendance.objects.filter(
                student=student,
                group=group,
                date=date
            ).exists()
            if not attendance_exists:
                Attendance.objects.create(
                    student=student,
                    group=group,
                    date=date,
                    present=present
                )
        messages.success(request, "Davomat muvaffaqiyatli qo'shildi.")
    else:
        messages.error(request, "Talabalarni olishda xato yuz berdi.")

    return redirect('admin_panel:attendances')

@login_required
@require_POST
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    present = request.POST.get('present') == '1'

    attendance.present = present
    attendance.save()

    messages.success(request, "Davomat muvaffaqiyatli yangilandi.")
    return redirect('admin_panel:attendances')

@login_required
@require_POST
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.delete()
    messages.success(request, "Davomat muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:attendances')

@login_required
@require_GET
def get_students(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    serialized_students = [
        {'id': student.id, 'fullname': student.fullname}
        for student in students
    ]
    return JsonResponse({'students': serialized_students})
##########################################################################################################
# ATTENDANCE END

# EVALUATIONS START
##########################################################################################################
@login_required
def evaluations(request):
    evaluations = Evaluation.objects.select_related('student', 'group').all()
    groups = Group.objects.all()
    return render(request, "baholash.html", {'evaluations': evaluations, 'groups': groups})

@login_required
@require_POST
def add_evaluation(request):
    group_id = request.POST.get('group')
    student_id = request.POST.get('student')
    date = request.POST.get('date')
    score = request.POST.get('score')
    feedback = request.POST.get('feedback', '')

    if not group_id or not student_id or not date or not score:
        messages.error(request, "Barcha maydonlar to'ldirilishi kerak.")
        return redirect('admin_panel:evaluations')

    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, id=student_id)

    if not group.students.filter(id=student.id).exists():
        messages.error(request, "Tanlangan talaba guruhga tegishli emas.")
        return redirect('admin_panel:evaluations')

    try:
        score = int(score)
        if not (0 <= score <= 10):
            raise ValueError
    except ValueError:
        messages.error(request, "Baho 1 dan 10 gacha bo'lishi kerak.")
        return redirect('admin_panel:evaluations')

    evaluation_exists = Evaluation.objects.filter(
        student=student,
        group=group,
        date=date
    ).exists()
    if evaluation_exists:
        messages.error(request, "Bu guruh, talaba va sana uchun baho allaqachon mavjud.")
        return redirect('admin_panel:evaluations')

    Evaluation.objects.create(
        group=group,
        student=student,
        date=date,
        score=score,
        feedback=feedback
    )

    messages.success(request, "Baho muvaffaqiyatli qo'shildi.")
    return redirect('admin_panel:evaluations')

@login_required
@require_POST
def edit_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)

    group_id = request.POST.get('group')
    student_id = request.POST.get('student')
    date = request.POST.get('date')
    score = request.POST.get('score')
    feedback = request.POST.get('feedback', '')

    if not group_id or not student_id or not date or not score:
        messages.error(request, "Barcha maydonlar to'ldirilishi kerak.")
        return redirect('admin_panel:evaluations')

    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, id=student_id)

    if not group.students.filter(id=student.id).exists():
        messages.error(request, "Tanlangan talaba guruhga tegishli emas.")
        return redirect('admin_panel:evaluations')

    try:
        score = int(score)
        if not (1 <= score <= 10):
            raise ValueError
    except ValueError:
        messages.error(request, "Baho 1 dan 10 gacha bo'lishi kerak.")
        return redirect('admin_panel:evaluations')

    evaluation_exists = Evaluation.objects.filter(
        student=student,
        group=group,
        date=date
    ).exclude(id=evaluation.id).exists()
    if evaluation_exists:
        messages.error(request, "Bu guruh, talaba va sana uchun baho allaqachon mavjud.")
        return redirect('admin_panel:evaluations')

    evaluation.group = group
    evaluation.student = student
    evaluation.date = date
    evaluation.score = score
    evaluation.feedback = feedback
    evaluation.save()

    messages.success(request, "Baho muvaffaqiyatli yangilandi.")
    return redirect('admin_panel:evaluations')

@login_required
@require_POST
def delete_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    evaluation.delete()
    messages.success(request, "Baho muvaffaqiyatli o'chirildi.")
    return redirect('admin_panel:evaluations')

@login_required
@require_GET
def get_students_evaluation(request, group_id):
    """
    Fetch students belonging to a specific group via AJAX for Evaluation.
    Returns JSON response with student IDs and fullnames.
    """
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    serialized_students = [
        {'id': student.id, 'fullname': student.fullname}
        for student in students
    ]
    return JsonResponse({'students': serialized_students})
##########################################################################################################
# EVALUATIONS END

class WeekDayViewSet(viewsets.ModelViewSet):
    queryset = WeekDay.objects.all()
    serializer_class = WeekDaySerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetAllStudentsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentNoPhoneSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
class BlogsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
