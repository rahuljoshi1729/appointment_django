from django.urls import path,include
from sche import views
urlpatterns = [
    path('signup/',views.registration_api.as_view(),name='signup'),
    path('login/',views.login_api.as_view(),name='login'),
    path('list/<str:type>/',views.ListAPI.as_view()),
    path('password/reset/',views.PasswordResetView.as_view(),name="password reset"),
    path('password/reset/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
