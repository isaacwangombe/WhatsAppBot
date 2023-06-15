from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=30, null=True, blank=True)
    phoneId = models.CharField(max_length=200, null=True, blank=True)

    # Utility Variable
    uniqueId = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)


class BusinessPlan(models.Model):
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    company_description = models.TextField(null=True, blank=True)

    # Utility Variable
    uniqueId = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(BusinessPlan, self).save(*args, **kwargs)

    @classmethod
    def get_all(cls, fromId):
        table = BusinessPlan.objects.filter(profile__phoneNumber=fromId)
        return table


class ChatSession(models.Model):
    OPTIONS = [
        ('Private', 'Private'),
        ('Partnership', 'Partnership'),
        ('Non-Profit', 'Non-Profit'),
    ]

    business_name = models.TextField(null=True, blank=True)
    business_type = models.CharField(
        choices=OPTIONS, max_length=100, null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    product_service = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    years = models.TextField(null=True, blank=True)
    progress = models.TextField(null=True, blank=True)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)

    # Utility Variable
    uniqueId = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(ChatSession, self).save(*args, **kwargs)
