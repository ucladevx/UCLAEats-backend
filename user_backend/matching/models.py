from django.db import models
from django.utils.translation import ugettext_lazy as _

from user_backend.users.models import User
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

# multiple dining halls, multiple times
class WaitingUser(models.Model):
    user = models.ForeignKey('User', on_delete=models.Cascade)
    start_time = models.DateTimeField(_('start_time'))
    end_time = models.DateTimeField(_('end_time'))
    dining_halls = models.TextField(
            _('dining_halls'), 
            max_length=2,
            choices=DINING_HALL_CHOICES,
            default=BPLATE,
    )

    class Meta:
        order = ('id',)

    def save(self, *args, **kwargs):
        self.dining_halls 
