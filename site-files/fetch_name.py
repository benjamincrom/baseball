import re
import requests

names = [x.strip() for x in open('names.txt','r').readlines()]

cantprint = []
for name in names:
    name2 = None
    webname = name.replace(' ', '+')
    response = requests.get(f'https://www.google.com/search?q=mlb+{webname}')
    namedict = re.findall(r">([\w ]+) Stats, Age, Position", response.text)
    if namedict:
        name2 = namedict[0]
    else:
        namedict = re.findall(r">([\w ]+) #\d+ - [\w ]+ - MLB\.com<", response.text)
        if namedict:
            name2 = namedict[0]
        else:
            cantprint.append(name)

    if name2:
        print(f"elif player_key == '{name}':")
        print(f"    player = self.find_player('{name2}')")

print()
print()
for name in cantprint:
    print(name)
