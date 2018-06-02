from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    # visible user data
    email = models.EmailField(_('email'), max_length=255, unique=True)
    first_name = models.CharField(_('first_name'), max_length=40, blank=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True)
    major = models.CharField(_('major'), max_length=150, blank=True)
    minor = models.CharField(_('minor'), max_length=150, blank=True)
    year = models.IntegerField(_('year'), default=0, null=True, blank=True)
    self_bio = models.TextField(_('self_bio'), blank=True)
    # profile_pic = models.ImageField(upload_to='profile_pictures/', null=True,
    #         blank=True)

    # non-visible user data
    is_on_chat = models.BooleanField(_('is_on_chat'), default=False)
    device_id = models.CharField(_('device_id'), max_length=150, blank=True, 
            default="")

    # Metadata fields, automatically has primary key ID
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_admin = models.BooleanField(_('is_admin'), default=False)
    is_staff = models.BooleanField(_('staff status'),default=True)

    # Add email as the username field for auth purposes
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # set objects reference as UserManager
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('date_created',)

    def __str__(self):
        """
        If printed, return email address
        """
        return (self.email, self.first_name, self.last_name, self.major,
                self.minor, self.year, self.self_bio, self.date_created,
                self.date_updated, self.is_active, self.is_admin, self.is_staff)

    def get_full_name(self):
        """
        Return the full name of a user
        """
        fullname = "%s %s" % (self.first_name, self.last_name)
        return fullname.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Email user a message
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

