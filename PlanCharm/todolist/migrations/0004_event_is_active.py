# Generated by Django 5.0.1 on 2024-06-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_event_notified_alter_event_title_alter_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]