# Generated by Django 4.1.2 on 2022-12-17 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0012_alter_querytodoc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='querytodoc',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='querytodoc',
            name='doc',
            field=models.CharField(default='None', max_length=999),
        ),
    ]