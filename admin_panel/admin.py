from django.contrib import admin
from .models import (
    Student, Teacher, Group, Tariff, Evaluation, Payment, Course, WeekDay, Attendance, Blogs
)

admin.site.register(Blogs)

@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ['get_name']
    ordering = ['name']
    search_fields = ['name']

    def get_name(self, obj):
        return obj.__str__()
    get_name.short_description = "Hafta kuni"


# Kurs uchun admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# Tarif uchun admin
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']


# O'qituvchi uchun admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'image']
    search_fields = ['fullname']
    # image ixtiyoriy; qo'shimcha sozlashlar talab qilinmaydi


# Guruh uchun admin
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'course', 'teacher', 'start_date', 'end_date',
        'tariff', 'hours', 'duration', 'get_days_of_week'
    ]
    list_filter = ['teacher', 'tariff', 'course', 'days_of_week']
    search_fields = ['name', 'teacher__fullname', 'course__name']
    filter_horizontal = ['days_of_week']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('students', 'days_of_week')

    def get_days_of_week(self, obj):
        return ", ".join([str(day) for day in obj.days_of_week.all()])
    get_days_of_week.short_description = "Hafta kunlari"


# Talaba uchun admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'get_groups', 'phone1', 'phone2', 'phone3']
    search_fields = ['fullname', 'groups__name']
    list_filter = ['groups']
    filter_horizontal = ['groups']
    fields = ['fullname', 'image', 'groups', 'phone1', 'phone2', 'phone3']

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = "Guruhlar"


# To'lov uchun admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'amount', 'date', 'method']
    list_filter = ['group', 'date', 'method']
    search_fields = ['student__fullname', 'group__name']
    date_hierarchy = 'date'


# Baholash uchun admin
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'score']
    list_filter = ['group', 'score']
    search_fields = ['student__fullname', 'group__name', 'teacher__fullname']
    list_editable = ['score']  # Bahoni joyida tahrirlash imkoniyati
    actions = ['bulk_evaluate']

    def bulk_evaluate(self, request, queryset):
        # Yig'ma baholash uchun amal o'rnatilishi kerak
        self.message_user(request, "Yig'ma baholash amali hali amalga oshirilmagan.")
    bulk_evaluate.short_description = "Tanlangan talabalarni yig'ma baholash"
    
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'date', 'present']
    list_filter = ['group', 'date', 'present']
    search_fields = ['student__fullname', 'group__name']
    list_editable = ['present']
    date_hierarchy = 'date'
    
    # Optimize queryset to reduce database hits
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'group')
    
    # Optional: Add actions for bulk attendance updates
    actions = ['mark_present', 'mark_absent']
    
    def mark_present(self, request, queryset):
        updated = queryset.update(present=True)
        self.message_user(request, f"{updated} attendance records marked as present.")
    mark_present.short_description = "Mark selected records as Present"
    
    def mark_absent(self, request, queryset):
        updated = queryset.update(present=False)
        self.message_user(request, f"{updated} attendance records marked as absent.")
    mark_absent.short_description = "Mark selected records as Absent"