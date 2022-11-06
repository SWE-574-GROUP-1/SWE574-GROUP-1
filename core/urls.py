from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # path('', views.index, name="index"),
    path("", views.homepage, name="homepage"),
    path("register", views.register, name="register"),
]