# Generated by Django 5.0.8 on 2024-08-31 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Channel',
            new_name='channel',
        ),
    ]
