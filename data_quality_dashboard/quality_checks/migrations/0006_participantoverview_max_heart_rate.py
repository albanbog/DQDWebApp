# Generated by Django 5.1.1 on 2024-09-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quality_checks', '0005_remove_participantoverview_max_heart_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantoverview',
            name='max_heart_rate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
