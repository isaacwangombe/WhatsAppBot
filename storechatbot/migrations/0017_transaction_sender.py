# Generated by Django 4.0.2 on 2023-09-22 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storechatbot', '0016_transaction_date_transaction_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.profiles'),
        ),
    ]