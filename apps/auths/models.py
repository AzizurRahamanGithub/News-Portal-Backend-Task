from datetime import datetime, time, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import timedelta
import string
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from import_export.admin import ImportExportActionModelAdmin
now = timezone.now()
from django.contrib import admin

from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "user")
        extra_fields.setdefault("is_active", True)  # normal user active by default (change if you use verification)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)

    # normal user info
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Make email the login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # keep username required for AbstractUser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["role"], name="role_idx"),
            models.Index(fields=["created_at"], name="created_at_idx"),
        ]


class CustomUserAdmin(ImportExportActionModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'full_name')


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    push_token = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def is_otp_expired(self):
        if self.otp_created_at:
            return timezone.now() > self.otp_created_at + timedelta(minutes=10)
        return True

    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    def is_reset_token_expired(self):
        if self.reset_token_expires:
            return timezone.now() > self.reset_token_expires
        return True

    def generate_reset_token(self):
        self.reset_token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=32))
        self.reset_token_expires = timezone.now() + timedelta(minutes=5)
        self.save()
        return self.reset_token

    def __str__(self):
        return f"Profile of {self.user.email}"


class ContactMessage (models.Model):
    full_name= models.CharField(max_length=200)
    email= models.EmailField()
    subject= models.CharField(max_length=300)
    message= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name}-{self.subject}"


class HelpUsImprove(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="improving") 
    improve_message= models.TextField()
    
    def __str__(self):
        return f"{self.user.full_name}-{self.improve_message}"