from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class DiningTable(models.Model):

    BPLATE = 'B'
    FEAST = 'F'
    DENEVE = 'D'
    COVEL = 'C'
    DINING_HALLS = (
        (BPLATE, 'Bplate'),
        (FEAST, 'Feast'),
        (DENEVE, 'Deneve'),
        (COVEL, 'Covel')
    )
    dining_hall = models.CharField(max_length=1, choices=DINING_HALLS)

    datetime = models.DateTimeField()

    users = ArrayField(models.IntegerField())

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    BREAKFAST = 'BF'
    LUNCH = 'LU'
    DINNER = 'DI'
    BRUNCH = 'BR'
    LATE_NIGHT = 'LN'
    MEAL_PERIOD_OPTIONS = (
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
        (BRUNCH, 'Brunch'),
        (LATE_NIGHT, 'LateNight')
    )
    meal_period = models.CharField(max_length=2, choices=MEAL_PERIOD_OPTIONS)

    creator_id = models.IntegerField()

    def __unicode__(self):
        return 'Time: ' + str(datetime) + ', Dining hall: ' + str(dining_hall)


"""
class Message(models.Model):
    room = models.ForeignKey(DiningTable, related_name='messages', on_delete=models.CASCADE,)
    sender = models.ForeignKey('users.User', on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.TextField()

    USER_MSG = 'U'
    SYSTEM_MSG = 'S'
    MSG_TYPES = (
        (USER_MSG, 'UserMessage'),
        (SYSTEM_MSG, 'SystemMessage')
    )
    message_type = models.CharField(max_length=1, choices=MSG_TYPES, default=USER_MSG)

    def __unicode__(self):
        return '[{timestamp}] {sender}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'sender': self.sender, 'message': self.message, 'timestamp': self.formatted_timestamp}
"""