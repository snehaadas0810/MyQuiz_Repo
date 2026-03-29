from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),

    path('create/', views.create_subject, name='create_subject'),

    # ✅ FIXED (no conflict now)
    path('detail/<int:subject_id>/', views.subject_detail, name='subject_detail'),

    path('<int:subject_id>/create-quiz/', views.create_quiz, name='create_quiz'),

    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),

    path('<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
]