# Generated by Django 4.2.7 on 2023-12-03 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('cart', '0003_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='products',
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.purchase')),
            ],
        ),
    ]