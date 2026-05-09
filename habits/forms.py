from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Habit


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["title", "description"]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Habit name",
                "class": "form-input"
            }),
            "description": forms.TextInput(attrs={
                "placeholder": "Description",
                "class": "form-input"
            }),
        }