from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manage import CustomeUserManager
# Create your models here.



class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomeUserManager()
    def __str__(self):
        return self.email

