from django.db import models
from django.conf import settings
from constants.roles import Roles
from users.models import User

class Institute(models.Model):
    institute_name = models.CharField(max_length=100)
    institute_city = models.CharField(max_length=50)
    institute_code = models.CharField(unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='institute'
    )

    def __str__(self):
        return self.institute_name