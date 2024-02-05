from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetailsManager(models.Manager):
    def get_active_users(self):
        return self.filter(is_active=True)


class UserDetail(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    date_of_joining = models.DateTimeField(auto_now_add=True)
    # Add any other fields you need
    objects = UserDetailsManager()

    def __str__(self):
        return self.name
