from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone 

from .model_constants import *

# Create your models here.

# multiple dining halls, multiple times
class WaitingUser(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    meal_times = ArrayField(models.DateTimeField(_('meal_times')))
    meal_day = models.DateField(_('meal_day'))
    meal_period = models.CharField(
            _('meal_period'),
            max_length = 2,
            choices = MEAL_PERIOD_CHOICES,
            default = DINNER,
    )
    dining_halls = ArrayField(
            models.CharField(
                _('dining_halls'),
                max_length=2,
                choices=DINING_HALL_CHOICES,
                default=BPLATE,
            )
    )
    found_match = models.BooleanField(_('found_match'), default=False)

    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    class Meta:
        ordering = ('id',)

class MatchedUsers(models.Model):
    user1 = models.ForeignKey('users.User', on_delete=models.CASCADE,
            related_name="user1")
    user2 = models.ForeignKey('users.User', on_delete=models.CASCADE,
            related_name="user2")
    meal_datetime = models.DateTimeField(_('meal_datetime'), 
            default = timezone.now)
    meal_period = models.CharField(
            _('meal_period'),
            max_length = 2,
            choices = MEAL_PERIOD_CHOICES,
            default = DINNER,
    )
    dining_hall = models.CharField(
            _('dining_hall'),
            max_length=2,
            choices=DINING_HALL_CHOICES,
            default=BPLATE,
    )
    chat_url = models.TextField(_('chat_url'), default="")

    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    class Meta:
        ordering = ('id',)
