from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.

FEAST = "FE"
BPLATE = "BP"
COVEL = "CO"
DENEVE = "DN"

DINING_HALL_CHOICES = (
    (FEAST, "FEAST"),
    (BPLATE, "BPLATE"),
    (COVEL, "COVEL"),
    (DENEVE, "DENEVE"),
)

BREAKFAST = "BR"
LUNCH = "LU"
DINNER = "DI"
LATENIGHT = "LN"

MEAL_PERIOD_CHOICES = (
    (BREAKFAST, "BREAKFAST"),
    (LUNCH, "LUNCH"),
    (DINNER, "DINNER"),
    (LATENIGHT, "LATENIGHT"),
)

# multiple dining halls, multiple times
class WaitingUser(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    times = ArrayField(models.DateTimeField(_('times')))
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

    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    class Meta:
        ordering = ('id',)

class MatchedUsers(models.Model):
    user1 = models.ForeignKey('users.User', 
            on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey('users.User', 
            on_delete=models.CASCADE, related_name="user2")
    time = models.DateTimeField(_('time'))
    meal_period = models.CharField(
            _('meal_period'),
            max_length = 2,
            choices = MEAL_PERIOD_CHOICES,
            default = DINNER,
    )
    dining_hall = models.CharField(
            _('dining_halls'),
            max_length=2,
            choices=DINING_HALL_CHOICES,
            default=BPLATE,
    )

    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    class Meta:
        ordering = ('id',)
