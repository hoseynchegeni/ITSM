# Generated by Django 4.2.7 on 2023-12-08 10:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0021_remove_task_task"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="creator",
            new_name="created_by",
        ),
    ]
