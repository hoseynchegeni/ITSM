# Generated by Django 4.2.6 on 2023-11-16 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("db_events", "0003_tasklog_task"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tasklog",
            name="record_id",
        ),
    ]
