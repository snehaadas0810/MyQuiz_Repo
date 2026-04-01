from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("subjects/", include("subjects.urls")),
    path("questions/", include("questions.urls")),
    path("results/", include("results.urls")),
]
