from django.urls import path
from . import views
urlpatterns = [
    path('secret/', views.SecretView.as_view())
]