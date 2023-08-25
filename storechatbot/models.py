from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os


class Profiles(models.Model):
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
        super(Profiles, self).save(*args, **kwargs)


class Apartment(models.Model):
    number = models.CharField(max_length=10, blank=True, null=True)
    monthly_rent = models.IntegerField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    # Other fields for apartment information

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
        super(Apartment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Apartment {self.number} - {self.property.name}"


class Renter(models.Model):
    profile = models.ForeignKey(
        Profiles, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    # Other fields for renter information

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
        super(Renter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class PropertyManager(models.Model):
    profile = models.ForeignKey(
        Profiles, on_delete=models.CASCADE, null=True, blank=True)

    # Other fields for property manager information

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
        super(PropertyManager, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class RepairRequest(models.Model):

    StatusOptions = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    renter = models.ForeignKey(
        Renter, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, null=True, blank=True)
    transaction_code = models.CharField(max_length=500, null=True, blank=True)
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


class Transaction(models.Model):
    transaction_code = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    recipient_name = models.CharField(max_length=100)
    recipient_account = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(ChatSession, self).save(*args, **kwargs)


class RenterPayment(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment = models.DateTimeField(null=True, blank=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.CharField(max_length=100, null=True, blank=True)
    payment_regularity = models.CharField(max_length=50)
    # Other fields for payment information

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
        super(RenterPayment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.renter}"


class ChatSession(models.Model):
    OPTIONS = [
        ('payment', 'payment'),
        ('receipt', 'receipt'),
        ('complaint', 'complaint'),
    ]

    chat_purpose = models.CharField(
        choices=OPTIONS, max_length=100, null=True, blank=True)

    profile = models.ForeignKey(
        Profiles, on_delete=models.CASCADE, null=True, blank=True)

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


class Message(models.Model):

    one = models.CharField(max_length=500, null=True, blank=True)
    two = models.CharField(max_length=500, null=True, blank=True)
    three = models.CharField(max_length=500, null=True, blank=True)

    # Utility Variables
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
