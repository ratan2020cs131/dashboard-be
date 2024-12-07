from django.db import models
from constants.roles import Roles

class Institute(models.Model):
    institute_name = models.CharField(max_length=100)
    institute_city = models.CharField(max_length=50)
    institute_code = models.CharField(unique=True)

    def __str__(self):
        return self.institute_name

