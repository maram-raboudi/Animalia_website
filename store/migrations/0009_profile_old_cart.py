# Generated by Django 5.0.2 on 2024-05-11 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_profile_delete_animal'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]