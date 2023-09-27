from django.db import models
from django.db.models import (
    CharField,
    ForeignKey,
    DateTimeField,
    TextField,
    IntegerField,
    BooleanField,
    ManyToManyField,
    FileField,
    OuterRef,
    Subquery,
    CASCADE,
    SET_NULL,
)
import uuid, pytz, json, os, uuid
from django.db.models import F
from datetime import datetime, timedelta


class PlayerRank(models.Model):
    # the league source is fantasy_pros
    created_at = DateTimeField(null=True, blank=True)
    last_updated = DateTimeField(null=True, blank=True)
    source = TextField(null=True, blank=True)
    league_scoring_type = TextField(null=True, blank=True)
    rank = IntegerField(null=True)
    fantasy_pros_id = IntegerField(null=True)
    full_name = TextField(null=True, blank=True)
    first_name = TextField(null=True, blank=True)
    last_name = TextField(null=True, blank=True)
    team_name_abbreviation = TextField(null=True, blank=True)
    player_position = TextField(null=True, blank=True)
    player_image = TextField(null=True, blank=True)
    player_yahoo_id = TextField(null=True, blank=True)
    player_bye_week = TextField(null=True, blank=True)
    sleeper_id = TextField(null=True, blank=True)
    ranking_timescale = TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        date = datetime.now(tz=pytz.utc)
        if not self.created_at:
            self.created_at = date.astimezone(pytz.timezone("America/Chicago"))

        self.last_updated = date.astimezone(pytz.timezone("America/Chicago"))

        super(PlayerRank, self).save(*args, **kwargs)

    def __str__(self):
        if not self.full_name or self.full_name == "":
            return "No Title"
        return self.full_name


class Messages(models.Model):
    # the league source is fantasy_pros
    created_at = DateTimeField(null=True, blank=True)
    email_address = TextField(null=True, blank=True)
    message = TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        date = datetime.now(tz=pytz.utc)
        if not self.created_at:
            self.created_at = date.astimezone(pytz.timezone("America/Chicago"))

        super(Messages, self).save(*args, **kwargs)
