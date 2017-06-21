# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"))

    def __str__(self):
        return _("Chat with ") + self.opponent.username


def get_user_image_folder(instance, filename):
    return "chatImages/%s/%s" %(instance.sender.id, filename)

class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages")
    text = models.TextField(verbose_name=_("Message text"), null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=get_user_image_folder)
    all_objects = models.Manager()

    def get_formatted_create_datetime(self):
        return dj_date(self.created, settings.DATETIME_FORMAT)

    def __str__(self):
        return str(self.id)
        #return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"
