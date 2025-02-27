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
    path("deny", views.deny, name="deny"),
    path("approve", views.approve, name="approve"),
    path("lost", views.lost, name="lost"),
    path("card", views.card, name="card"),
    path("citizen", views.citizen, name="citizen"),
    path("applicant", views.applicant, name="applicant"),
    path("applicant/<int:id>", views.applicant_show, name="applicant.show"),
    path("province", views.province, name="province"),
    path("commune", views.commune, name="commune"),
    path("colline", views.colline, name="colline"),
    path("my-card", views.my_card, name="my-card"),
    path("lost-cards", views.lost_cards, name="lost-cards"),
    path("notification", views.notification, name="notification"),
    # dashboard
    path("dashboard", views.dashboard, name="dashboard"),
    path("settings", views.settings, name="settings"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/<int:id>/update", views.profile_update, name="profile.update"),
]
