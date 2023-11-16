# Generated by Django 4.2.6 on 2023-11-16 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0013_taskprioritychange"),
        ("db_events", "0002_tasklog"),
    ]

    operations = [
        migrations.AddField(
            model_name="tasklog",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="log",
                to="tasks.task",
            ),
        ),
    ]
