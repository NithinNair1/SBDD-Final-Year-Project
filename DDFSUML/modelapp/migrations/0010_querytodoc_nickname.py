# Generated by Django 4.0.2 on 2022-11-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0009_alter_querytodoc_listosymp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='querytodoc',
            name='nickname',
            field=models.CharField(default='John Doe', max_length=555),
        ),
    ]