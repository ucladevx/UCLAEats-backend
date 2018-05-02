from django.db import models

from user_backend.users.models import User
# Create your models here.

class WaitingUser(models.Model):
    user = models.ForeignKey('User', on_delete=models.Cascade)
     
