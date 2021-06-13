from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordResetView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]