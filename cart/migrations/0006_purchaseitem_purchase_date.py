# Generated by Django 4.2.7 on 2024-02-06 14:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_purchaseitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
