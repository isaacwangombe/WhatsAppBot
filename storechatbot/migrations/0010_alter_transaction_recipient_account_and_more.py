# Generated by Django 4.0.2 on 2023-09-12 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0009_chatsession_question_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient_account',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_code',
            field=models.CharField(max_length=100),
        ),
    ]
