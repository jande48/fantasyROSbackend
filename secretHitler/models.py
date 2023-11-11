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
import random


class Game(models.Model):
    # the league source is fantasy_pros
    created_at = DateTimeField(null=True, blank=True)
    last_updated = DateTimeField(null=True, blank=True)
    code = TextField(null=True, blank=True)
    num_of_players = TextField(null=True, blank=True)

    def getNumOfLiberalsFascists(self):
        if self.num_of_players == 5:
            return 3, 1
        if self.num_of_players == 6:
            return 4, 1
        if self.num_of_players == 7:
            return 4, 2
        if self.num_of_players == 8:
            return 5, 2
        if self.num_of_players == 9:
            return 5, 3
        if self.num_of_players == 0:
            return 6, 3
        return 0, 0

    def save(self, *args, **kwargs):
        date = datetime.now(tz=pytz.utc)
        if not self.created_at:
            self.created_at = date.astimezone(pytz.timezone("America/Chicago"))
        self.last_updated = date.astimezone(pytz.timezone("America/Chicago"))
        if not self.code:
            # Import string and random module
            import string
            import random

            def getChar():
                return random.choice(string.ascii_letters)

            # Randomly choose a letter from all the ascii_letters
            self.code = f"{getChar()}{getChar()}{getChar()}{getChar()}"

            other_games = Game.objects.filter(code=self.code)
            if other_games.count() > 0:
                other_games.delete()

        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        if not self.code or self.code == "":
            return "No Code"
        return self.code


class Player(models.Model):
    # the league source is fantasy_pros
    created_at = DateTimeField(null=True, blank=True)
    last_updated = DateTimeField(null=True, blank=True)
    name = TextField(null=True, blank=True)
    vote = TextField(null=True, blank=True)
    party = TextField(null=True, blank=True)
    role = TextField(null=True, blank=True)
    game = ForeignKey(
        Game,
        related_name="player",
        on_delete=CASCADE,
        null=True,
    )

    def save(self, *args, **kwargs):
        date = datetime.now(tz=pytz.utc)
        if not self.created_at:
            self.created_at = date.astimezone(pytz.timezone("America/Chicago"))
        self.last_updated = date.astimezone(pytz.timezone("America/Chicago"))

        if not self.role and not self.party:
            num_of_liberals, num_of_fascists = self.game.getNumOfLiberalsFascists()
            num_of_liberals = (
                num_of_liberals
                - Player.objects.filter(game=self.game, party="liberal").count()
            )
            num_of_fascists = (
                num_of_fascists
                - Player.objects.filter(game=self.game, party="fascist")
                .exclude(role="hitler")
                .count()
            )
            num_of_hilter = 1 - Player.objects.filter(role='hitler').count()

            player_obj = []
            for x in range(num_of_liberals):
                player_obj.append('liberal')
            for x in range(num_of_fascists):
                player_obj.append('fascist')
            for x in range(num_of_hilter):
                player_obj.append('hitler')
            
            self.role = random.choice(player_obj)
            if self.role == 'hitler':
                self.party = 'fascist'
            else:
                self.party = self.role
            

        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        if not self.name or self.name == "":
            return "No Name"
        return self.name
