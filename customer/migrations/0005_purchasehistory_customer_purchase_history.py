# Generated by Django 4.1.1 on 2022-09-14 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_cart_alter_product_id'),
        ('customer', '0004_customer_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(default=django.db.models.functions.datetime.Now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='purchase_history',
            field=models.ManyToManyField(related_name='purchase_history', through='customer.PurchaseHistory', to='store.product'),
        ),
    ]