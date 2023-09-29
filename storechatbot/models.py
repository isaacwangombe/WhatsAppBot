from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os


class Apartment(models.Model):
    StatusOptions = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
        ('VeryLate', 'VeryLate'),
    ]
    number = models.CharField(max_length=10, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(
        choices=StatusOptions, max_length=100, null=True, blank=True)
    occupied = models.BooleanField(default=False, blank=True, null=True)
    monthly_rent = models.IntegerField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    # Other fields for apartment information

    # Utility Variable
    uniqueId = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


class RepairMen(models.Model):

    RepairManTypes = [
        ('General', 'General'),
        ('Plumbing', 'Plumbing'),
        ('Carpentry', 'Carpentry'),
        ('Electric', 'Electric'),
        ('Masonry', 'Masonry'),
        ('Metalwork', 'Metalwork'),
    ]
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(
        choices=RepairManTypes, max_length=100, null=True, blank=True)
    # Other fields for apartment information

    # Utility Variable
    uniqueId = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


class Profiles(models.Model):
    RoleOptions = [
        ('Owner', 'Owner'),
        ('Manager', 'Manager'),
        ('Renter', 'Renter')
    ]
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phoneNumber = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    phoneId = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(
        choices=RoleOptions, max_length=100, null=True, blank=True)
    payment_regularity = models.IntegerField(null=True, blank=True)

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


class RepairRequest(models.Model):

    StatusOptions = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    Ratings = [
        ('1', 'Very Poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent'),
    ]

    RepairTypes = [
        ('1', 'Plumbing'),
        ('2', 'Electric'),
        ('3', 'Carpentry'),
        ('4', 'Masonry'),
        ('5', 'Metalwork'),
        ('6', 'General'),

    ]
    renter = models.ForeignKey(
        Profiles, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(choices=RepairTypes,
                            max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        choices=StatusOptions, max_length=100, null=True, blank=True)
    repair_cost = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(choices=Ratings, blank=True, null=True)
    review = models.IntegerField(blank=True, null=True)
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
    message = models.CharField(max_length=500, blank=True, null=True)
    sender = models.ForeignKey(
        Profiles, on_delete=models.CASCADE, blank=True, null=True)
    transaction_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    recipient_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_account = models.CharField(max_length=200, blank=True, null=True)

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
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_code


class ChatSession(models.Model):
    OPTIONS = [
        ('payment', 'payment'),
        ('receipt', 'receipt'),
        ('complaint', 'complaint'),
        ('create', 'create'),
    ]

    chat_purpose = models.CharField(
        choices=OPTIONS, max_length=100, null=True, blank=True)
    question_no = models.IntegerField(default=0)

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
