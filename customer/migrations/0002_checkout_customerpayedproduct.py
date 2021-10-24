# Generated by Django 3.1.4 on 2021-01-03 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('payment_id', models.CharField(default=None, max_length=255, null=True)),
                ('total_amount', models.FloatField()),
                ('payment_singnature', models.CharField(default=None, max_length=255, null=True)),
                ('reciept_num', models.CharField(max_length=255)),
                ('delivery_address', models.CharField(max_length=2000)),
                ('delivery_phoone', models.CharField(max_length=20)),
                ('payment_completed', models.BooleanField()),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPayedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('product_description', models.CharField(max_length=2000)),
                ('checkout_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.checkout')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
