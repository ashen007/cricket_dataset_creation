import requests
import urllib3


class Players:
    def __init__(self, link):
        self.player_page = link

    def getter(self, player):
        """
        read url and return content
        :param player: player name
        :return: content
        """
        player_url = self.player_page + player
        respond = requests.get(player_url)

        if respond.status_code == 200:
            return respond.content
        elif respond.status_code == 404:
            print('Not found.')
        elif respond.status_code == 500:
            print('Internal error.')

    def get_player_stat(self, player):
        stat_page = self.player_page + player + '/bowling-batting-stats'
        respond = requests.get(stat_page)

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
