# Generated by Django 4.0.2 on 2023-09-12 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0011_alter_transaction_amount_alter_transaction_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='date',
        ),
    ]
