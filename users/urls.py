from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('validate/', views.validate_user, name='validate_user'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path(
        'register/validate/', views.register_create, name='register_validate'
    ),
]
