# Generated by Django 3.2.5 on 2021-12-23 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_seeing_conversations_seen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversations',
            old_name='date',
            new_name='date_time',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='create',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='date',
            new_name='date_time',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='seeing',
            new_name='seen',
        ),
    ]