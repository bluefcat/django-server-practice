from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

# Create your models here.

class Member(AbstractUser):
    objects = UserManager()

    #username
    #first_name
    #last_name
    #email
    #password
    #groups
    #user_permission
    #is_staff
    #is_active
    #is_superuser
    #last_login
    #date_joined

    nickname = models.CharField(max_length=32)
    #자기소개 부분
    profile = models.TextField(blank=True, max_length=200)
    phone = models.CharField(max_length=16)
    
    profile_image = models.ImageField(blank=True, null=True)

    def __repr__(self):
        return f"{self.id}: {self.nickname}"

