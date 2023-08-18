from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.

class User(AbstractBaseUser):
    phone=models.CharField(max_length=11,unique=True)
    username=models.CharField(max_length=255,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=('email','username')

    objects=UserManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class OTP(models.Model):
    phone=models.CharField(max_length=11)
    code=models.SmallIntegerField()

    def __str__(self) -> str:
        return str(self.code)
