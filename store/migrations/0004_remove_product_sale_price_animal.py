# Generated by Django 5.0.2 on 2024-04-26 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_category_options_product_is_sale_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=6)),
                ('description', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('image', models.ImageField(upload_to='uploads/animal/')),
                ('is_sale', models.BooleanField(default=False)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
    ]