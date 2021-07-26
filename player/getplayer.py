import requests
import urllib.error as error
import urllib.parse as urlparse
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer  #


class Players:
    def __init__(self):
        self.player_page = 'https://www.espncricinfo.com'

    def get_player_dtl(self, country, player):
        """
        read url and return content
        :param player: player name
        :return: content
        """
        player_url = urlparse.urljoin(f'{self.player_page}/player/', player)

        try:
            respond = requests.get(player_url)
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

        if respond.status_code == 200:
            return respond.content
        elif respond.status_code == 404:
            print('Not found.')
        elif respond.status_code == 500:
            print('Internal error.')

    def get_player_stat(self, player):
        stat_page = urlparse.urljoin(self.player_page, f'/player/{player}/bowling-batting-stats')

        try:
            respond = requests.get(stat_page)
        except error.URLError as e:
            print('Error Occurred: ', e.reason)

        if respond.status_code == 200:
            return respond.content
        elif respond.status_code == 404:
            print('Not found.')
        elif respond.status_code == 500:
            print('Internal error.')


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
    countries = {tag.text: tag.get('href') for tag in country_pages[1:-3]}

    return countries[country]
