# Generated by Django 4.2.5 on 2023-10-01 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0008_alter_venue_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(
                blank=True, related_name="attendees", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="manager",
            field=models.ForeignKey(
                default=events.models.get_superuser,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="manager",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
