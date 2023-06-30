from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4


class Message(models.Model):
    Message = models.TextField(null=True, blank=True)

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
        super(Message, self).save(*args, **kwargs)


class Transactions(models.Model):
    Message = models.ForeignKey(
        Message, null=True, blank=True, on_delete=models.CASCADE)
    quatity = models.CharField(null=True, blank=True, max_length=100)
    transactionCode = models.CharField(null=True, blank=True, max_length=100)
    date = models.CharField(null=True, blank=True, max_length=100)

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
        super(Transactions, self).save(*args, **kwargs)


class RepairRequest(models.Model):

    StatusOptions = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Closed', 'Closed'),
    ]
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        choices=StatusOptions, max_length=100, null=True, blank=True)
    repairCost = models.IntegerField(blank=True, null=True)
    # Other fields for repair request information

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
        super(RepairRequest, self).save(*args, **kwargs)

    def __str__(self):
        return f"Repair Request for {self.apartment}"
