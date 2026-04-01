from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_student, name="register"),
    path("register/teacher/", views.register_teacher, name="register_teacher"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/students/", views.manage_students, name="manage_students"),
    path("approve/<int:user_id>/", views.approve_student, name="approve_student"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("register/teacher/", views.register_teacher, name="register_teacher"),
    path("teacher/profile/", views.teacher_profile, name="teacher_profile"),
    path("update-email/", views.update_email, name="update_email"),
    path("change-password/", views.change_password, name="change_password"),
    path("student/profile/", views.student_profile, name="student_profile"),
]
