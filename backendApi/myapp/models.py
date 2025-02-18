from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class MyAppManager(BaseUserManager):
    def create_user(self, name, email, password, mobile):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            mobile=mobile
        )
        user.password = make_password(password)  # Hash password properly
        user.save(using=self._db)
        return user

class MyApp(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  

    objects = MyAppManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email
