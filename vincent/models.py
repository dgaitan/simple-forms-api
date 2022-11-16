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


class Form(BaseModel):
    """Form Model"""

    class Statuses(models.IntegerChoices):
        DRAFT = 1, _('Draft')
        PUBLISHED = 2, _('Published')
        TRASHED = 3, _('Trashed')

    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('Define a Name to your form')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
        help_text=_('Give a description to your form if necessary')
    )
    status = models.IntegerField(
        _('Status'),
        blank=True,
        default=Statuses.DRAFT,
        choices=Statuses.choices
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        on_delete=models.CASCADE,
        blank=True
    )

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def __str__(self):
        return self.name
