# Generated by Django 4.1.2 on 2022-12-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0013_querytodoc_complete_querytodoc_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='querytodoc',
            name='docnote',
            field=models.TextField(blank=True),
        ),
    ]
