import requests
from bs4 import BeautifulSoup
import re, json
import urllib.request
from rankings.models import PlayerRank
from rankings.utils import getPlayerData


def updateRankings(URL, league_scoring_type):
    with urllib.request.urlopen(URL) as web:
        soup = BeautifulSoup(web.read(), "lxml")
        pattern = re.compile('var ecrData = (.*?);(?=[^"]*(?:(?:"[^"]*){2})*$)')
        script = soup.find("script", text=pattern)
        if not script:
            print("no script")
            return

        match = pattern.findall(script.text)
        if not match:
            print("no match")
            return
        try:
            data = json.loads(match[0].strip())

        except Exception as e:
            print("problem", e)
            return
        sleeper_player_data = getPlayerData()

        def try_another_way(sleeper_player, fantasy_pros_player):
            try:
                fantasy_pros_player_name_formatted = (
                    fantasy_pros_player["player_name"]
                    .replace(" ", "")
                    .replace(",", "")
                    .replace("'", "")
                    .replace(".", "")
                    .replace("-", "")
                    .replace("Jr", "")
                    .replace("III", "")
                    .strip()
                    .lower()
                )
                sleeper_player_name_formatted = (
                    sleeper_player["search_full_name"]
                    .replace(" ", "")
                    .replace(",", "")
                    .replace("'", "")
                    .replace(".", "")
                    .replace("-", "")
                    .replace("Jr", "")
                    .replace("III", "")
                    .strip()
                    .lower()
                )
                if (
                    sleeper_player_name_formatted == fantasy_pros_player_name_formatted
                    and sleeper_player_data[key]["position"]
                    == fantasy_pros_player.player_position_id
                ):
                    return True
                return False
            except:
                return False

        for i, p in enumerate(data["players"]):
            player_obj, created = PlayerRank.objects.get_or_create(
                fantasy_pros_id=p["player_id"],
                league_scoring_type=league_scoring_type,
                source="fantasy_pros",
            )
            player_obj.rank = i + 1
            player_obj.full_name = p["player_name"]
            player_obj.team_name_abbreviation = p["player_team_id"]
            player_obj.player_position = p["player_position_id"]
            player_obj.player_image = p["player_image_url"]
            player_obj.player_yahoo_id = p["player_yahoo_id"]
            player_obj.player_bye_week = p["player_bye_week"]
            for key in sleeper_player_data.keys():
                if p["player_position_id"] == "DST":
                    fantasy_pros_def_name = p["player_name"].replace(" ", "").lower()
                    if sleeper_player_data[key]["position"] == "DEF":
                        sleeper_def_name = f"{sleeper_player_data[key]['first_name']}{sleeper_player_data[key]['last_name']}".replace(
                            " ", ""
                        ).lower()
                        if fantasy_pros_def_name == sleeper_def_name:
                            player_obj.sleeper_id = str(
                                sleeper_player_data[key]["player_id"]
                            )
                try:
                    yahoo_id = str(sleeper_player_data[key]["yahoo_id"])
                except:
                    if try_another_way(sleeper_player_data[key], p):
                        player_obj.sleeper_id = str(
                            sleeper_player_data[key]["player_id"]
                        )
                if p["player_yahoo_id"] == yahoo_id:
                    player_obj.sleeper_id = str(sleeper_player_data[key]["player_id"])
                else:
                    if try_another_way(sleeper_player_data[key], p):
                        player_obj.sleeper_id = str(
                            sleeper_player_data[key]["player_id"]
                        )
                if p["player_name"] == "Dak Prescott":
                    player_obj.sleeper_id = "3294"
                if "dobbins" in p["player_name"].lower():
                    player_obj.sleeper_id = "6806"
            player_obj.save()
        print(f"updated {league_scoring_type} rankings")


def updateAllRankings():
    PlayerRank.objects.all().delete()
    ppr_url = "https://www.fantasypros.com/nfl/rankings/ros-ppr-overall.php"
    updateRankings(ppr_url, "ppr")
    half_url = "https://www.fantasypros.com/nfl/rankings/ros-half-point-ppr-overall.php"
    updateRankings(half_url, "half")
    std_url = "https://www.fantasypros.com/nfl/rankings/ros-overall.php"
    updateRankings(std_url, "std")
