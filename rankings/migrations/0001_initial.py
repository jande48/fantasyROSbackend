# Generated by Django 4.2.5 on 2023-09-11 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('league_scoring_type', models.TextField(blank=True, null=True)),
                ('rank', models.IntegerField(null=True)),
                ('fantasy_pros_id', models.IntegerField(null=True)),
                ('full_name', models.TextField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('team_name_abbreviation', models.TextField(blank=True, null=True)),
                ('player_position', models.TextField(blank=True, null=True)),
                ('player_image', models.TextField(blank=True, null=True)),
                ('player_yahoo_id', models.TextField(blank=True, null=True)),
                ('player_bye_week', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
