from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from common.managers import CustomUserManager

PHONE_NUMBER_REGEX = RegexValidator(
    r"(254|0)(1|7)([0-9])([0-9])([0-9])([0-9])([0-9])([0-9])([0-9])([0-9])",
    "Phone number should be in the format 254712234345",
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(validators=[PHONE_NUMBER_REGEX], max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_subscribers(self):
        users = User.objects.all()
        users = users.exclude(pk=self.pk)
        return users
