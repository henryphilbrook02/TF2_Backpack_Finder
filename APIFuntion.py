import requests
import itertools

class SteamAIP:

    def __init__(self, newSKey, newBPKey):
        self.sKey = newSKey
        self.bpKey = newBPKey

    def hasPlayed(self, id):  # Only work for one id
        response = requests.get(
            'http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=' + self.sKey + '&steamid=' + id + '&format=json&include_appinfo=0&include_played_free_games=1').json()
        ans = True
        if 'games' in response['response']:
            games = response['response']['games']
            for gid in games:
                if gid['appid'] == 440 and 'playtime_2weeks' not in gid:
                    ans = False
        return ans

    def getFriendslist(self, id):  # only work for one id
        response = requests.get(
            'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + self.sKey + '&steamid=' + id + '&relationship=friend').json()
        idList = []
        if 'friendslist' in response:
            friendList = response['friendslist']['friends']
            for dict in friendList:
                idList.append(dict['steamid'])
        return idList

    def getProfUrl(self, ids): #paramater must be in a list this max is also 100
        returnList = []
        cdString = ",".join(ids)
        response = requests.get(
            'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + self.sKey + '&steamids=' + cdString).json()
        player = response['response']['players']
        for dict in player:
            returnList.append([dict['steamid'], dict['profileurl']])
        returnList.sort()
        return returnList

    def hasWorth(self, ids, refPrice, minVal): # max of 100 ids per request
        cdString = ",".join(ids)
        response = requests.get('https://backpack.tf/api/users/info/v1?key='+ self.bpKey +'&steamids='+ cdString)
        json = response.json()
        returnList = []
        for id in ids:
            # First checks to see if the backpack is there then makes sure the bp is valuable enough
            if 'inventory' in json['users'][id]:
                if '440' in json['users'][id]['inventory']:
                    if 'value' in json['users'][id]['inventory']['440']:
                        if json['users'][id]['inventory']['440']['value']*refPrice >= minVal:
                            worth = json['users'][id]['inventory']['440']['value']*refPrice
                            worth = "%.2f" % worth
                            returnList.append([id, str(worth)])
        return returnList



def delDups(array):
    array.sort()
    return list(array for array,_ in itertools.groupby(array))
