# Generated by Django 4.0.2 on 2023-08-22 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storechatbot', '0003_message_repairrequest_transactions_delete_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('monthly_rent', models.IntegerField(blank=True, null=True)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_purpose', models.CharField(blank=True, choices=[('payment', 'payment'), ('receipt', 'receipt'), ('complaint', 'complaint')], max_length=100, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('phoneId', models.CharField(blank=True, max_length=200, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storechatbot.apartment')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='RenterPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_payment', models.DateTimeField(blank=True, null=True)),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_code', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_regularity', models.CharField(max_length=50)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storechatbot.apartment')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storechatbot.renter')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_code', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('recipient_name', models.CharField(max_length=100)),
                ('recipient_account', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='Message',
        ),
        migrations.RemoveField(
            model_name='repairrequest',
            name='description',
        ),
        migrations.AddField(
            model_name='message',
            name='one',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='three',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='two',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='repairrequest',
            name='transaction_code',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='repairrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Closed', 'Closed')], max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
        migrations.AddField(
            model_name='chatsession',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.profiles'),
        ),
        migrations.AddField(
            model_name='repairrequest',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.apartment'),
        ),
        migrations.AddField(
            model_name='repairrequest',
            name='renter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storechatbot.renter'),
        ),
    ]