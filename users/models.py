from django.db import models
from constants.roles import Roles

class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    onboarding = models.IntegerField(default=0)
    role = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=Roles.choices(),
        default=None
    )

    def __str__(self):
        return self.email
