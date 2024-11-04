# admin_panel/models.py

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Haftaning kunlari modeli
class WeekDay(models.Model):
    DAY_CHOICES = [
        (1, 'Dushanba'),
        (2, 'Seshanba'),
        (3, 'Chorshanba'),
        (4, 'Payshanba'),
        (5, 'Juma'),
        (6, 'Shanba'),
        (7, 'Yakshanba'),
    ]
    name = models.IntegerField(
        choices=DAY_CHOICES,
        unique=True,
        verbose_name="Hafta kuni"
    )

    def __str__(self):
        return dict(self.DAY_CHOICES).get(self.name, "Noma'lum kun")

    class Meta:
        verbose_name = "Hafta kuni"
        verbose_name_plural = "Hafta kunlari"
        ordering = ['name',]


# Kurslarni boshqarish uchun Model
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        indexes = [
            models.Index(fields=['name']),
        ]


# Tariflar modelini yaratish
class Tariff(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tarif nomi")
    price = models.IntegerField(verbose_name="Narx")

    def __str__(self):
        return f"{self.name} - {self.price} so'm"

    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tariflar"
        indexes = [
            models.Index(fields=['name']),
        ]


# O'qituvchi modelini yaratish
class Teacher(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="To'liq ism")
    image = models.ImageField(upload_to="photos/", verbose_name="Foto", blank=True, null=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"
        indexes = [
            models.Index(fields=['fullname']),
        ]


# Guruh modelini yaratish
class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name="Guruh nomi")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups', verbose_name="O'qituvchi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups', verbose_name="Kurs")
    start_date = models.DateField(verbose_name="O'qish boshlanish sanasi")
    end_date = models.DateField(verbose_name="O'qish tugash sanasi")
    lesson_start_time = models.CharField(
        max_length=5, 
        verbose_name="Dars boshlanish vaqti", 
        choices=[("08:00", "08:00"), ("08:30", "08:30"), ("09:00", "09:00"), ("09:30", "09:30"),
                 ("10:00", "10:00"), ("10:30", "10:30"), ("11:00", "11:00"), ("11:30", "11:30"),
                 ("12:00", "12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"),
                 ("14:00", "14:00"), ("14:30", "14:30"), ("15:00", "15:00"), ("15:30", "15:30"),
                 ("16:00", "16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"),
                 ("18:00", "18:00"), ("18:30", "18:30"), ("19:00", "19:00"), ("19:30", "19:30"),
                 ("20:00", "20:00")], 
        help_text="Masalan: 08:00"
    )
    lesson_end_time = models.CharField(
        max_length=5, 
        verbose_name="Dars tugash vaqti", 
        choices=[("08:00", "08:00"), ("08:30", "08:30"), ("09:00", "09:00"), ("09:30", "09:30"),
                 ("10:00", "10:00"), ("10:30", "10:30"), ("11:00", "11:00"), ("11:30", "11:30"),
                 ("12:00", "12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"),
                 ("14:00", "14:00"), ("14:30", "14:30"), ("15:00", "15:00"), ("15:30", "15:30"),
                 ("16:00", "16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"),
                 ("18:00", "18:00"), ("18:30", "18:30"), ("19:00", "19:00"), ("19:30", "19:30"),
                 ("20:00", "20:00")], 
        help_text="Masalan: 08:00"
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='groups', verbose_name="Tarif")
    days_of_week = models.ManyToManyField(WeekDay, related_name='groups', verbose_name="Hafta kunlari")
    hours = models.PositiveIntegerField(verbose_name="Darslar soni", help_text="Umumiy darslar soni")
    duration = models.PositiveIntegerField(verbose_name="Dars davomiyligi (min)", help_text="Dars davomiyligi daqiqalarda")

    def __str__(self):
        return f"{self.name}: {self.course.name} _ {self.lesson_start_time} -> {self.lesson_end_time} ||| {self.start_date} -> {self.end_date}"

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        indexes = [
            models.Index(fields=['name']),
        ]


# Talaba modelini yaratish
class Student(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="To'liq ism")
    image = models.ImageField(upload_to="photos/", verbose_name="Foto", blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='students', verbose_name="Guruhlar")
    phone1 = models.CharField(max_length=20, verbose_name="Telefon 1")
    phone2 = models.CharField(max_length=20, verbose_name="Telefon 2", blank=True, null=True)
    phone3 = models.CharField(max_length=20, verbose_name="Telefon 3", blank=True, null=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
        indexes = [
            models.Index(fields=['fullname']),
        ]


# Baholash modelini yaratish
class Evaluation(models.Model):
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='evaluations', 
        verbose_name="Guruh"
    )
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='evaluations', 
        verbose_name="Talaba"
    )
    date = models.DateField(verbose_name="Baholash sanasi")
    score = models.PositiveIntegerField(verbose_name="Baho", help_text="0 - 10")
    feedback = models.TextField(verbose_name="Fikr-mulohaza", blank=True, null=True)

    def __str__(self):
        return f"{self.student.fullname}: {self.score}"

    def clean(self):
        if not (0 <= self.score <= 10):
            raise ValidationError('Baho 0 dan 10 gacha bo\'lishi kerak.')

    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Baholar"
        constraints = [
            models.UniqueConstraint(fields=['student', 'group'], name='unique_evaluation_per_student_per_group')
        ]
        indexes = [
            models.Index(fields=['student', 'group']),
        ]


# To'lov modelini yaratish
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Naqt', 'Naqt'),
        ('Karta orqali', 'Karta orqali'),
        ('Payme orqali', 'Payme orqali'),
    ]

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='payments', 
        verbose_name="Talaba"
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='payments', 
        verbose_name="Guruh"
    )
    amount = models.IntegerField(verbose_name="Summasi")
    date = models.DateField(auto_now_add=True, verbose_name="To'lov sanasi")
    method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        verbose_name="To'lov usuli", 
        help_text="Naqt, Karta orqali, Payme orqali"
    )

    def __str__(self):
        return f"{self.student.fullname} - {self.group.name} - {self.amount} so'm - {self.date} - {self.method}"

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        indexes = [
            models.Index(fields=['student', 'group', 'date']),
        ]


# Davomat modelini yaratish
class Attendance(models.Model):
    STATUS_CHOICES = [
        (True, "Darsga keldi"),
        (False, "Darsga kelmadi"),
    ]

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='attendances', 
        verbose_name="Talaba"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="Guruh"
    )
    date = models.DateField(verbose_name="Dars sanasi")
    present = models.BooleanField(
        choices=STATUS_CHOICES,
        verbose_name="Davomat",
        default=True
    )

    def __str__(self):
        status = "Keldi" if self.present else "Kelmadi"
        return f"{self.student.fullname} - {self.date}: {status}"

    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomatlar"
        constraints = [
            models.UniqueConstraint(fields=['student', 'group', 'date'], name='unique_attendance_per_student_per_group_per_date')
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['student']),
            models.Index(fields=['group']),
        ]

class Blogs(models.Model):
    title = models.CharField(max_length=100, verbose_name="Sarlavha")
    image = models.ImageField(upload_to="blogs/", verbose_name="Rasm")
    short_desc = models.CharField(max_length=100, verbose_name="Qisqa izoh")
    desc = models.TextField(verbose_name="Tavsif")
    author = models.CharField(max_length=100, verbose_name="Muallif")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Bloglar"
        verbose_name_plural = "Bloglar"