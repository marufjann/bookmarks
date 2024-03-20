from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    # url-адреса входа и выхода

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # url-адреса смены пароля
    path('password-change/', auth_views.PasswordChangeView.as_view(),
         name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # url-адреса сброса пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uid64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('', views.dashboard, name='dashboard'),
]
