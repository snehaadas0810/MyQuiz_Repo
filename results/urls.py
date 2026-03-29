from django.urls import path
from . import views
from .views import student_results

urlpatterns = [
    path('', views.all_results, name='all_results'),
    path('student/', views.student_results, name='student_results'),
    path('review/<int:result_id>/', views.review_result, name='review_result'),
    path('student/results/', student_results, name='student_results'),
]