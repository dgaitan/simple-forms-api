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


class FormField(models.Model):
    """Form Fields"""
    class FieldTypes(models.IntegerChoices):
        TEXT = 1, _('Text')
        TEXTAREA = 2, _('Textarea')
        NUMBER = 3, _('Number')
        SELECT = 4, _('Select')
        CHECKBOX = 5, _('Checkbox')
        RADIO = 6, _('Radio')

    form = models.ForeignKey(
        Form,
        verbose_name=_('Form'),
        on_delete=models.CASCADE
    )
    field_type = models.IntegerField(
        _('Field Type'),
        blank=True,
        default=FieldTypes.TEXT,
        choices=FieldTypes.choices
    )
    label = models.CharField(
        _('Label'),
        help_text=_('Define a label'),
        max_length=255
    )
    placeholder = models.CharField(
        _('Placeholder'),
        help_text=_('Add a placeholder if needed'),
        max_length=255,
        blank=True,
        null=True
    )
    required = models.BooleanField(
        _('Is Field Required?'),
        default=False,
        blank=True
    )

    class Meta:
        verbose_name = _('Form Field')
        verbose_name_plural = _('Form Fields')

    def __str__(self):
        return self.label
    