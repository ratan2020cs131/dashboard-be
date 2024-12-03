from django.db import models
from enum import Enum

class RoleEnum(Enum):
    STUDENT = 'student'
    FACULTY = 'faculty'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'

    @classmethod
    def choices(cls):
        return [(key.value, key.value.title()) for key in cls]

class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=RoleEnum.choices(),
        default=RoleEnum.STUDENT.value
    )
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email
