# TF2_Backpack_Finder
Backpack price finder: (Run the GUI.py to start the program)

![image](https://user-images.githubusercontent.com/63463905/136314401-80c128a1-f130-4016-a455-b2bea077a6db.png)

This is the simple GUI that you need to fill out here are what the fields mean:
Steam API ID: This is the API key linked with your steam account you can register for one at this link: https://partner.steamgames.com/doc/webapi_overview/auth
BP.tf API ID Key: This is for backpack.tf which is a database / website that has prices for each item in the game. If the website is still active you will be able to get the key here: https://backpack.tf/developer
Starting Steam Profile ID: This is a ID that steam assigns your account with, this ID does not have to be yours but here is how to find it: https://support.nexon.net/hc/en-us/articles/360001118286-How-do-I-find-my-Steam-ID-
Levels of Search: This is how many levels you want this program to run. At 1 level the program will get the friends of all the people on the given ID's friend list then get each friend’s friend list and go through and look up their inventory worth. At level 2 it will pick a friend on the ID's friend list at random and do the same thing again. Level 3 will do the same thing again ... and so on.
Minimum Value: This is the minimum value that you want a backpack to have. If you only want inventories at or over $300, put 300 in that box.
All the inventories found will be output in the SteamDB.accdb which is an access database file for those who do not know. I realize not everyone will have an access DB account but there are free accdb readers and this data can be imported into excel.

