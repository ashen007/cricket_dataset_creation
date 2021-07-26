import requests
import json
import os
import pandas as pd
import urllib.error as error
import urllib.parse as urlparse

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer  #


class Players:
    def __init__(self, country, level='INTERNATIONAL'):
        self.player_page = 'https://www.espncricinfo.com'
        self.country = country
        self.level = level

    @property
    def __player_links__(self):
        if not os.path.exists(f'../data/{self.country}/player_link_{self.level}.pkl'):
            get_players(self.country, self.level)

        return pd.read_pickle(f'../data/{self.country}/player_link_{self.level}.pkl')

    def get_player_dtl(self, player):
        """
        read url and return content
        :param player: player name
        :return: content
        """
        player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        player_url = urlparse.urljoin('https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId=',
                                      player.values[0])

        try:
            respond = requests.get(player_url).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

    def get_player_stat(self, player):
        player = self.__player_links__[self.__player_links__['longName'] == player]['objectId']
        stat_page = urlparse.urljoin('https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats?playerId=',
                                     player.values[0])

        try:
            respond = requests.get(stat_page).json()
            return respond
        except error.URLError as e:
            print('Error Occurred: ', e.reason)


class Test:
    """
    get test records for specific player
    """

    def __init__(self, name):
        self.name = name

    def get(self):
        print('get player records.')

    def save(self):
        print('save player records.')


class OneDay:
    """
    get on day international records for specific player
    """

    def __init__(self, name):
        self.name = name

    def get(self):
        print('get player records.')

    def save(self):
        print('save player records.')


class T20:
    """
    get twenty-twenty international records for specific player
    """

    def __init__(self, name):
        self.name = name

    def get(self):
        print('get player records.')

    def save(self):
        print('save player records.')


class ASeries:
    """
    get A-series records for specific player
    """

    def __init__(self, name):
        self.name = name

    def get(self):
        print('get player records.')

    def save(self):
        print('save player records.')


class FirstClass:
    """
    get first class records for specific player
    """

    def __init__(self, name):
        self.name = name

    def get(self):
        print('get player records.')

    def save(self):
        print('save player records.')


def get_records_on(format='test', name=None):
    """
    get player records
    :param format:
    :param name:
    :return:
    """
    formats = dict(test=Test(name),
                   odi=OneDay(name),
                   t20=T20(name),
                   aseries=ASeries(name),
                   firstclass=FirstClass(name))
    return formats[format]


def get_countries(country):
    player_page = 'https://www.espncricinfo.com/player/'
    respond = requests.get(player_page).content
    nav = SoupStrainer('nav')
    sub_nav = bs(respond, 'lxml', parse_only=nav).find('nav', attrs={'class': 'sub-navbar'})
    country_pages = sub_nav.find_all('a', attrs={'class': 'nav-link'})
    countries = {tag.text: tag.get('href') for tag in country_pages[1:-2]}

    return countries[country]


def get_players(country, level='INTERNATIONAL'):
    RECORDS = 9999
    country_page = get_countries(country)[-1]

    base = f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/search?mode=BOTH&page=1&records={RECORDS}'
    country_filter = f'&filterTeamId={country_page}&'
    format_level_filter = f'filterFormatLevel={level}&sort=ALPHA_ASC&filterActive=true'
    full_url = base + country_filter + format_level_filter

    respond = requests.get(full_url).json()
    link_list = [[player['objectId'],
                  player['longName'],
                  f'{player["slug"]}-{player["objectId"]}'] for player in respond['results']]
    link_list = pd.DataFrame(link_list, columns=['objectId', 'longName', 'link'])

    try:
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
