from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
]
