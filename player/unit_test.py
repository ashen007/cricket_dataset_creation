import getplayer

player = getplayer.Players('https://www.espncricinfo.com/player/')

print(player.getter('joe-burns-326632'))