# Generated by Django 4.0.2 on 2023-06-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
