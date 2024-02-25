from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('verify/', views.EmailVerification.as_view()),
    path('user_details/',views.UserDetails.as_view() )
]
