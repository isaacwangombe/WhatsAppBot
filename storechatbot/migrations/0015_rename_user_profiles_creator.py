# Generated by Django 4.0.2 on 2023-09-13 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0014_remove_apartment_renter_apartment_occupied_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profiles',
            old_name='user',
            new_name='creator',
        ),
    ]