from django import forms
from .models import *

class GroupForm(forms.ModelForm):
    days_of_week = forms.ModelMultipleChoiceField(
        queryset=WeekDay.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'course', 'start_date', 'end_date', 
                  'lesson_start_time', 'lesson_end_time', 'tariff', 
                  'days_of_week', 'hours', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lesson_start_time': forms.Select(attrs={'class': 'form-control'}),
            'lesson_end_time': forms.Select(attrs={'class': 'form-control'}),
            'tariff': forms.Select(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': "Kurs Nomi",
            'description': "Tavsif",
        }

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['fullname', 'image']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'group', 'amount', 'method']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'group': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'method': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'student': "Talaba",
            'group': "Guruh",
            'amount': "Summasi (so'm)",
            'method': "To'lov Usuli",
        }