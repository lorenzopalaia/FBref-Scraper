import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from datetime import date
import requests
from bs4 import BeautifulSoup

LEAGUE_STATS_MAP = {
    0 : "/league_table_overall.csv",
    1 : "/league_table_homeaway.csv",
    2 : "/standard_stats_squad.csv",
    3 : "/standard_stats_opponent.csv",
    4 : "/goalkeeping_squad.csv",
    5 : "/goalkeeping_opponent.csv",
    6 : "/advanced_goalkeeping_squad.csv",
    7 : "/advanced_goalkeeping_opponent.csv",
    8 : "/shooting_squad.csv",
    9 : "/shooting_opponent.csv",
    10 : "/passing_squad.csv",
    11 : "/passing_opponent.csv",
    12 : "/pass_types_squad.csv",
    13 : "/pass_types_opponent.csv",
    14 : "/goal_shot_creation_squad.csv",
    15 : "/goal_shot_creation_opponent.csv",
    16 : "/defensive_actions_squad.csv",
    17 : "/defensive_actions_opponent.csv",
    18 : "/possession_squad.csv",
    19 : "/possession_opponent.csv",
    20 : "/playing_time_squad.csv",
    21 : "/playing_time_opponent.csv",
    22 : "/misc_squad.csv",
    23 : "/misc_opponent.csv"
}

LEAGUES = {
    9: 'Premier-League-Stats',
    11: 'Serie-A-Stats',
    12: 'La-Liga-Stats',
    13: 'Ligue-1-Stats',
    20: 'Bundesliga-Stats',
}


def get_cur_season():
    cur_year = date.today().year
    if date.today().month in range(8, 13):
        return '{cur_year}-{next_year}'.format(cur_year = cur_year, next_year = cur_year + 1)
    elif date.today().month in range(1, 9):
        return '{prev_year}-{cur_year}'.format(prev_year = cur_year - 1, cur_year = cur_year)

def download_league_csv(league_id, season = ''):
    league_name = LEAGUES[league_id]
    cur_season = False
    if season == '':
        cur_season = True
        season = get_cur_season()
    path = 'csv/leagues/{league_name}/{season}'.format(league_name = league_name, season = season)
    if not os.path.exists(path):
        os.makedirs(path)
    dfs = None
    if cur_season:
        dfs = pd.read_html('https://fbref.com/en/comps/{league_id}/{league_name}'.format(
            league_id = league_id,
            league_name = league_name,
        ))
    else:
        dfs = pd.read_html('https://fbref.com/en/comps/{league_id}/{season}/{season}-{league_name}'.format(
            league_id = league_id,
            league_name = league_name,
            season = season
        ))
    for id in LEAGUE_STATS_MAP.keys():
        dfs[id].to_csv('{path}/{stat_name}'.format(path = path, stat_name = LEAGUE_STATS_MAP[id]))

'''
def download_big5_season_csv(season = ''):
    for key in LEAGUES.keys():
        download_league_csv(key, season)
'''

def get_league_teams(league_id, season = ''):
    league_name = LEAGUES[league_id]
    cur_season = False
    if season == '':
        cur_season = True
        season = get_cur_season()
    url = None
    if cur_season:
        url = 'https://fbref.com/en/comps/{league_id}/{league_name}'.format(
            league_id = league_id,
            league_name = league_name,
        )
    else:
        url = 'https://fbref.com/en/comps/{league_id}/{season}/{season}-{league_name}'.format(
            league_id = league_id,
            league_name = league_name,
            season = season
        )
    r = requests.get(url).text
    bs = BeautifulSoup(r, 'html.parser')
    table = bs.find('table', id=lambda x: x and x.startswith('result'))
    teams = []
    urls = []
    for a in table.findAll('a'):
        if a.parent.name == 'td' and a.parent.attrs['data-stat'] == 'team':
            teams.append(a.string)
            urls.append(a['href'])
    df = pd.DataFrame()
    df['Team'] = teams
    df['URL'] = urls
    return df

def get_player_stats(player):
    df = pd.read_html(player)[0]
    
    headers = []
    for h in list(df.columns.values):
        n = h[1]
        if h[0] == 'Per 90 Minutes':
            n = '{header}/P90'.format(header = h[1])
        headers.append(n)
    df.columns = headers    
    df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
    df = df.drop('Matches', axis=1)
    return df

def download_league_players_stats(league_id, season = ''):
    league_name = LEAGUES[league_id]
    cur_season = False
    if season == '':
        cur_season = True
        season = get_cur_season()
    path = 'csv/leagues/{league_name}/{season}/all_players.csv'.format(league_name = league_name, season = season)
    df = None
    if cur_season:
        df = get_league_teams(league_id, '')
    else:
        df = get_league_teams(league_id, season)
    frames = []
    for url in df['URL']:
        frames.append(get_player_stats('{base}{url}'.format(base = 'https://fbref.com', url = url)))
    df = pd.concat(frames)
    df = df.reset_index()
    df = df.drop('index', axis=1)
    df.to_csv(path)


download_league_csv(11, '')
download_league_csv(11, '2021-2022')
download_league_players_stats(11, '')
download_league_players_stats(11, '2021-2022')


'''
#TEST AREA

def get_team_players(team):
    r = requests.get(team).text
    bs = BeautifulSoup(r, 'html.parser')
    table = bs.find('div', id='div_stats_standard_11')
    names = []
    urls = []
    for a in table.findAll('a'):
        if a.parent.name == 'th':
            names.append(a.string)
            urls.append(a['href'])
    df = pd.DataFrame()
    df['Name'] = names
    df['URL'] = urls
    return df

def get_league_players_urls(league):
    df = get_league_teams(league)
    frames = []
    for url in df['URL']:
        frames.append(get_team_players('{base}{url}'.format(base = BASE_URL, url = url)))
    df = pd.concat(frames)
    return df

#get_team_players('https://fbref.com/en/squads/cf74a709/Roma-Stats')
#get_league_players_urls('https://fbref.com/en/comps/11/Serie-A-Stats')
'''