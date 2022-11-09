from django.db import models

# Create your models here.

class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=16)

    joindate = models.DateField(auto_now_add=True)

    #멤버 비활성화
    inactive = models.BooleanField()

    def __repr__(self):
        return f"{self.id}: {self.nickname}"

