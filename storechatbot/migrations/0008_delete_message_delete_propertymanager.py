# Generated by Django 4.0.2 on 2023-09-06 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0007_profiles_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='PropertyManager',
        ),
    ]