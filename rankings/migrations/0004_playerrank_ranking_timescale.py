# Generated by Django 4.2.5 on 2023-09-27 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0003_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerrank',
            name='ranking_timescale',
            field=models.TextField(blank=True, null=True),
        ),
    ]
