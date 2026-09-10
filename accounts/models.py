from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,full_name,email,google_id=None,password=None,**extra_fields):
        if not email:
            raise TypeError("Email is Required!")

        user=self.model(full_name=full_name,email=self.normalize_email(email),google_id=google_id,**extra_fields)

        if password:
            user.set_password(password)

        else:
            user.set_unusable_password()

        user.save()

        return user

    def create_superuser(self,full_name,email,password):
        if not password:
            raise TypeError("Password is Required")

        user=self.create_user(full_name=full_name,email=email,password=password)
        user.is_staff=True
        user.is_superuser=True
        user.is_profile_complete=True
        user.save()

        return user

class User(AbstractBaseUser,PermissionsMixin):
    profile_picture=models.ImageField(upload_to='profile/',blank=True)
    full_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    google_id=models.CharField(max_length=255,null=True,blank=True,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)    
    is_profile_complete=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['full_name']

    objects=UserManager()

    def __str__(self):
        return f"{self.id}-{self.full_name}"    