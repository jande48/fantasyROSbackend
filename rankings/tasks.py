import requests
from bs4 import BeautifulSoup
import re, json
import urllib.request
from rankings.models import PlayerRank


def updateRankings(URL, league_scoring_type):
    with urllib.request.urlopen(URL) as web:
        soup = BeautifulSoup(web.read(), 'lxml')
        pattern = re.compile('var ecrData = (.*?);(?=[^"]*(?:(?:"[^"]*){2})*$)')
        script = soup.find("script",text=pattern)
        if not script:
            print('no script')
            return 

        match = pattern.findall(script.text)
        if not match:
            print('no match')
            return
        try:
            data = json.loads(match[0].strip())

        except Exception as e:
            print('problem',e)
            return
        
        for i,p in enumerate(data["players"]):
            player_obj, created = PlayerRank.objects.get_or_create(fantasy_pros_id=p['player_id'],league_scoring_type=league_scoring_type,source='fantasy_pros')
            player_obj.rank = i+1
            player_obj.full_name = p["player_name"]
            player_obj.team_name_abbreviation = p["player_team_id"]
            player_obj.player_position = p["player_position_id"]
            player_obj.player_image = p["player_image_url"]
            player_obj.player_yahoo_id = p["player_yahoo_id"]
            player_obj.player_bye_week = p["player_bye_week"]
            player_obj.save()
        print('updated PPR rankings')

def updateRankings():
    ppr_url = "https://www.fantasypros.com/nfl/rankings/ros-ppr-overall.php"
    updateRankings(ppr_url,'ppr')
    half_url = "https://www.fantasypros.com/nfl/rankings/ros-half-point-ppr-overall.php"
    updateRankings(half_url,'half')
    std_url = "https://www.fantasypros.com/nfl/rankings/ros-overall.php"
    updateRankings(std_url,'std')

