# Generated by Django 4.1.2 on 2022-11-21 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0010_querytodoc_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='querytodoc',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]