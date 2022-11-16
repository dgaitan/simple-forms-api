from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Primary Model Base
    
    Add here common fields related
    """
    created_at = models.DateTimeField(
        _('Created At'), 
        auto_now_add=True, 
        blank=True, 
        null=False
    )
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
        blank=True,
        null=False
    )

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """Default User"""

    def __str__(self):
        return self.username
