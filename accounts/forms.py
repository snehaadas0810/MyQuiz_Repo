from .models import User
from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.is_approved = False  # needs teacher approval
        if commit:
            user.save()
        return user


class TeacherRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "teacher"
        user.is_approved = True  # teachers are approved automatically
        if commit:
            user.save()
        return user
