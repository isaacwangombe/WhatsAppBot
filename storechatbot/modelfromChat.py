from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
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


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # Other fields for company information

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
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
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
        super(CompanyUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Property(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # Other fields for property information

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
        super(Property, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
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
        Profile, on_delete=models.CASCADE, null=True, blank=True)
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
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

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
        ('Ongoing', 'Ongoing'),
        ('Closed', 'Closed'),
    ]
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
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
        ('registration', 'registration'),
        ('complaint', 'complaint'),
    ]

    chat_purpose = models.CharField(
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
