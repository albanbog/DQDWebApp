# Generated by Django 5.1.1 on 2024-09-17 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quality_checks', '0008_sleeplog_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleeplog',
            name='logId',
            field=models.BigIntegerField(db_index=True, unique=True),
        ),
    ]
