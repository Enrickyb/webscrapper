from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

desired_leagues = ["LaLiga", "Premier League", "Serie A", "Coppa Italia", "Ligue 1",
                   "Copa do Mundo de Clubes", "Brasileirão", "UEFA Liga Europa",
                   "EUFA Liga dos Campeões", "CONMEBOL Libertadores", "Brasileirão Série B"]

def enterOnPageGame(gameid):
    url = "https://onefootball.com/pt-br/match/" + gameid
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html, "html.parser")

def getTvBroadcaster(tv_span):
    if tv_span:
        tv_broadcaster = tv_span.find_next("span", class_="title-8-regular")
        if tv_broadcaster:
            return tv_broadcaster.text
        else:
            return None
    else:
        return None
    
def getDate(date_span):
    if date_span:
        date = date_span.find_next("span", class_="title-8-regular")
        if date:
            return date.text
        else:
            return None
    else:
        return None   


def getLeague(league_span):
    if league_span:
        league = league_span.find_next("span", class_="title-8-regular")
        if league:
            return league.text
        else:
            return None
    else:
        return None  

def getTeamName():
    team_names = []
    gameid_elements = soup.find_all("a", class_="MatchCard_matchCard__iOv4G")

    for gameid_element in gameid_elements:
        gameid = gameid_element.get("href").split("/")[3]
        match_soup = enterOnPageGame(gameid)

        home_team = match_soup.find("span", class_="MatchScoreTeam_name__zzQrD")
        away_team = match_soup.find_all("span", class_="MatchScoreTeam_name__zzQrD")[1]
        tv_span = match_soup.find("span", class_="title-7-medium", text="Guia de TV")
        tv_broadcaster = getTvBroadcaster(tv_span)

        home_logo_url = match_soup.find_all("img", class_="EntityLogo_entityLogoImage__4X0wF")[1]["src"]
        away_logo_url = match_soup.find_all("img", class_="EntityLogo_entityLogoImage__4X0wF")[2]["src"]
        game_time = match_soup.find("span", class_="title-6-bold MatchScore_numeric__ke8YT").text
        league_logo_url = match_soup.find_all("img", class_="EntityLogo_entityLogoImage__4X0wF")[0]["src"]

        date_span = match_soup.find("span", class_="title-7-medium", text="Início")
        game_date = getDate(date_span)

        league_span = match_soup.find("span", class_="title-7-medium", text="Competição")
        league = getLeague(league_span)


        if home_team and away_team and tv_broadcaster and league in desired_leagues:
            team_names.append({
                "home": {
                    "name": home_team.text,
                    "logo_url": home_logo_url
                },
                "away": {
                    "name": away_team.text,
                    "logo_url": away_logo_url
                },
                "tv_broadcaster": tv_broadcaster,
                "game_time": game_time,
                "game_date": game_date,
                "league": league,
                "league_logo_url": league_logo_url
            })
    return team_names

@app.route('/api', methods=['GET'])
def api():
    date = request.args.get('date')
    url = "https://onefootball.com/pt-br/jogos" + "?date=" + date
    response = requests.get(url)
    html = response.text
    global soup
    soup = BeautifulSoup(html, "html.parser")
    result = getTeamName()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
