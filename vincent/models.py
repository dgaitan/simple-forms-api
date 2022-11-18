import re

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
        SELECT = 4, _('Dropdown')
        CHECKBOX = 5, _('Checkbox')
        RADIO = 6, _('Radio')
        EMAIL = 7, _('Email')
        DATE = 8, _('Date')
        TIME = 9, _('Time')

    form = models.ForeignKey(
        Form,
        verbose_name=_('Form'),
        on_delete=models.CASCADE,
        related_name='fields'
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
    name = models.CharField(
        _('Name'),
        max_length=500,
        blank=True
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

    def save(self, *args, **kwargs):
        if self.label:
            field_name = re.sub(r"[^\w\s-]", "", self.label.lower())
            self.name = re.sub(r"[-\s]+", "_", field_name).strip("-_")
        
        return super(FormField, self).save(*args, **kwargs)

    def __str__(self):
        return self.label

class Options(models.Model):
    field = models.ForeignKey(
        FormField,
        verbose_name=_('Field'),
        on_delete=models.CASCADE,
        related_name='options'
    )
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('Option Name')
    )
    order = models.IntegerField(
        _('Order'),
        default=1,
        blank=True
    )

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')
        ordering = ['-order']

    def __str__(self):
        return self.name


class Submission(BaseModel):
    """
    Submission

    It refers to every single submit on a form
    """
    form = models.ForeignKey(
        Form,
        verbose_name=_('Form'),
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')

    def __str__(self):
        return "Submission #{0} for {1}".format(self.pk, self.form.name)


class Answer(models.Model):
    """
    Answer

    This represents an answer on a form submission
    """
    submission = models.ForeignKey(
        Submission,
        verbose_name=_('Submission'),
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        FormField,
        verbose_name=_('Question'),
        on_delete=models.CASCADE,
        related_name='submission_answers'
    )
    answer = models.TextField(_('Answer'))

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return "Answer for: {}".format(self.question.label)