import requests
import json
import os
import pandas as pd
import urllib.error as error
import urllib.parse as urlparse

from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer  #


class Players:
    """
    abstract factory
    """

    def __init__(self, country, level, active):
        """
        initialize country
        :param country: player country
        :param level: format level
        """
        self.player_page = 'https://www.espncricinfo.com'
        self.country = country
        self.level = level
        self.active = active

    @property
    def __player_links__(self):
        """
        player links
        :return:
        """
        if not os.path.exists(f'../data/{self.country}/player_link_{self.level}.pkl'):
            get_players(self.country, self.level, self.active)

        return pd.read_pickle(f'../data/{self.country}/player_link_{self.level}.pkl')

    def get_player_dtl(self, player):
        """
        player details
        :param player: player name
        :return: content
        """
        # player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        player_url = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={player}'

        try:
            respond = requests.get(player_url).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

    def get_player_test_stat(self, player, playing_type):
        """
        player stata so far
        :param player: player id
        :return:
        """
        # player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        # https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary?playerId=50710&recordClassId=3&type=ALLROUND
        stat_page = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary?playerId={player}' \
                    f'&recordClassId={1}&type={playing_type}'

        try:
            respond = requests.get(stat_page).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

    def get_player_odi_stat(self, player, playing_type):
        """
        player stata so far
        :param player: player id
        :return:
        """
        # player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        stat_page = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary?playerId={player}' \
                    f'&recordClassId={2}&type={playing_type}'

        try:
            respond = requests.get(stat_page).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

    def get_player_t20_stat(self, player, playing_type):
        """
        player stata so far
        :param player: player id
        :return:
        """
        # player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        stat_page = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary?playerId={player}' \
                    f'&recordClassId={3}&type={playing_type}'

        try:
            respond = requests.get(stat_page).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)


def get_countries(country):
    """
    get countries
    :param country: country
    :return: country id
    """
    player_page = 'https://www.espncricinfo.com/player/'
    respond = requests.get(player_page).content
    nav = SoupStrainer('nav')
    sub_nav = BS(respond, 'lxml', parse_only=nav).find('nav', attrs={'class': 'sub-navbar'})
    country_pages = sub_nav.find_all('a', attrs={'class': 'nav-link'})
    countries = {tag.text: tag.get('href') for tag in country_pages[1:-2]}

    return countries[country]


def get_players(country, level, active):
    """
    request player ids
    :param active: active or not
    :param country: country
    :param level: format level
    :return: datafram
    """
    RECORDS = 9999
    country_page = get_countries(country)[-1]

    base = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/search?mode=BOTH&page=1&records={RECORDS}'
    country_filter = f'&filterTeamId={country_page}&'
    format_level_filter = f'filterFormatLevel={level}&sort=ALPHA_ASC&filterActive={active}'
    full_url = base + country_filter + format_level_filter

    respond = requests.get(full_url).json()
    link_list = [[player['objectId'],
                  player['longName'],
                  f'{player["slug"]}-{player["objectId"]}'] for player in respond['results']]
    link_list = pd.DataFrame(link_list, columns=['objectId', 'longName', 'link'])

    try:
        if not os.path.exists(f'../data'):
            os.makedirs(f'../data')

        if not os.path.exists(f'../data/{country}'):
            os.makedirs(f'../data/{country}')

        print(f'{country} folder created.')

    except OSError:
        print(f"can't create this /{country} folder.")

    try:
        with open(f'../data/{country}/player_{level}.json', 'w') as file:
            json.dump(respond, file)

        print(f'{country} players record successfully saved.')

    except FileNotFoundError:
        print('file not found.')

    try:
        with open(f'../data/{country}/player_link_{level}.pkl', 'wb') as links:
            link_list.to_pickle(links)

    except FileNotFoundError:
        print('file not found.')


def players_details(country, level='INTERNATIONAL', active=True):
    """
    get player stat and details then save them as json file
    :param active: player currently active
    :param country: country
    :param level: format level
    :return: json file
    """
    playing_types = ['BATTING', 'BOWLING', 'FIELDING', 'ALLROUND']
    country_players = Players(country, level, active)
    players = country_players.__player_links__

    for index in players['objectId']:
        dtl = country_players.get_player_dtl(index)

        if not os.path.exists(f'../data/{country}/Players'):
            os.makedirs(f'../data/{country}/Players')

        if not os.path.exists(f'../data/{country}/Players/{index}'):
            os.makedirs(f'../data/{country}/Players/{index}')

        for cat in playing_types:
            test = country_players.get_player_test_stat(index, cat)
            odi = country_players.get_player_odi_stat(index, cat)
            t20 = country_players.get_player_t20_stat(index, cat)

            with open(f'../data/{country}/Players/{index}/player_test_{cat}.json', 'w') as player_path:
                json.dump(test, player_path)

            with open(f'../data/{country}/Players/{index}/player_odi_{cat}.json', 'w') as player_path:
                json.dump(odi, player_path)

            with open(f'../data/{country}/Players/{index}/player_t20_{cat}.json', 'w') as player_path:
                json.dump(t20, player_path)

        player = {'player': dtl['player'],
                  'teams': dtl['content']['teams']}

        with open(f'../data/{country}/Players/{index}/player_dtl.json', 'w') as player_path:
            json.dump(player, player_path)
