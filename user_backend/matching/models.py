from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone 

from .model_constants import *

# Create your models here.

class Report(models.Model):
    reporting_user = models.ForeignKey('users.User', related_name="reporting_user", on_delete=models.CASCADE)
    reported_user = models.ForeignKey('users.User', related_name="reported_user", on_delete=models.CASCADE)
    chat_url = models.TextField(_('chat_url'), default="")
    details = models.TextField(_('details'), default="")
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

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

    status = models.CharField(
            _('status'),
            max_length=1,
            choices=REQUEST_STATUS_CHOICES,
            default=PENDING,
    )
    #found_match = models.BooleanField(_('found_match'), default=False)

    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    class Meta:
        ordering = ('id',)

class MatchedUsers(models.Model):
    user1 = models.ForeignKey('users.User', on_delete=models.CASCADE,
            related_name="user1")
    user2 = models.ForeignKey('users.User', on_delete=models.CASCADE,
            related_name="user2")
    user1_first_name = models.CharField(_('user1_first_name'), max_length=40, 
            blank=True)
    user1_last_name = models.CharField(_('user1_last_name'), max_length=150,
            blank=True)
    user2_first_name = models.CharField(_('user2_first_name'), max_length=40,
            blank=True)
    user2_last_name = models.CharField(_('user2_last_name'), max_length=150,
            blank=True)
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
