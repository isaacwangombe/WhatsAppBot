# Generated by Django 4.0.2 on 2023-09-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0006_remove_renterpayment_renter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='role',
            field=models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Manager', 'Manager'), ('Renter', 'Renter')], max_length=100, null=True),
        ),
    ]