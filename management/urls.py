from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
    # user authentication
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    # service & publication
    path("service", views.ServiceList.as_view(), name="services"),
    path("service/<int:pk>", views.ServiceDetail.as_view(), name="service"),
    path("publication", views.PublicationList.as_view(), name="publications"),
    path("publication/<int:pk>", views.PublicationDetail.as_view(), name="publication"),
    # application
    path("apply", views.apply, name="apply"),
]
