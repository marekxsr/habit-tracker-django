from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register_view, name="register"),

    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    path("add/", views.add_habit, name="add_habit"),   # URL pattern for adding a new habit

    path("delete/<int:habit_id>/", views.delete_habit, name="delete_habit"), # URL pattern for deleting a habit

    path("toggle/<int:habit_id>/<str:date>/",views.toggle_habit, name="toggle_habit"), # URL pattern for toggling habit completion status

]
