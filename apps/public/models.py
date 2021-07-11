from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class AccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password):
        username = uuid4()
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, username=username, email=email)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(first_name, last_name, email, password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.UUIDField(unique=True)
    profile_picture = models.ImageField(upload_to="account", default="account/user.png", blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    date_joined = models.DateField(default=timezone.now)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return False

    def has_perms(self, perm_list, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return False


class AccountVerification(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
