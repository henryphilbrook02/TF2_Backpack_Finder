import PySimpleGUI as sg
import DataBase
import random
import APIFuntion

run = True
steamKey = ""
bpKey = ""
startingSteamID = ""
maxLevel = 1  # this is the minimum amount to run once anything less will just be pointless
minValue = 0

while run:
    layout = [
        [sg.Text("Steam API ID:", size=(20, 1)), sg.InputText(steamKey)],
        [sg.Text("BP.tf API ID Key:", size=(20, 1)), sg.InputText(bpKey)],
        [sg.Text("Starting Steam Profile ID:", size=(20, 1)), sg.InputText()],
        [sg.Text("Levels of Search:", size=(20, 1)), sg.InputText(maxLevel)],
        [sg.Text("Minimum Value:", size=(20, 1)), sg.InputText(minValue)],
        [sg.Submit()]
    ]

    # Create the window
    window = sg.Window("TF2 Backpack Finder", layout)

    event, values = window.read()

    window.close()

    try:
        maxLevel = int(values[3])
        minValue = int(values[4])
    except Exception as e:
        print("This is supposed to be a number: ", e)
        exit()

    steamKey = str(values[0])  # string
    bpKey = str(values[1])  # String
    startingSteamID = str(values[2])  # String # this is curId in the code below

    apiClass = APIFuntion.SteamAIP(steamKey, bpKey)

    tempList = []  # used when breaking apart larger lists
    worthWhile = []  # ids of potential people to add
    urlList = []  # ids and worth without the urls yet
    dataList = []  # the list that will be added to the database
    # ^ id, worth, URL

    layout = [
        [sg.Text(size=(40, 1), key='-TASK-')],
        [sg.Text(size=(45, 1), key='-OUTPUT-')],
        [sg.ProgressBar(1, orientation='h', size=(35, 20), key='progress')]
    ]

    window = sg.Window('TF2 Backpack Finder', layout).Finalize()
    progress_bar = window.FindElement('progress')

    # This loop works by taking a friends list then going through each friend and getting their friend list
    # Then it determines if they are worthwhile then adds them to the worth while list
    window['-TASK-'].update("Searching For Backpacks:")
    levels = 1
    curId = startingSteamID  # srtarting curid
    while levels <= maxLevel:
        progress = 0
        friendsList = apiClass.getFriendslist(curId)
        curId = friendsList[random.randint(0, (len(friendsList) - 1))]
        for id in friendsList:
            outputTxt = str("Level: " + str(levels) + " |  ID: " + str(id))
            window['-OUTPUT-'].update(outputTxt)
            progress_bar.UpdateBar(progress, len(friendsList))
            innerFList = apiClass.getFriendslist(id)
            while len(innerFList) > 100:
                tempList = innerFList[:100]
                innerFList = innerFList[100:]
                worthWhile = worthWhile + apiClass.hasWorth(tempList, .04, minValue)
            worthWhile = worthWhile + apiClass.hasWorth(innerFList, .04, minValue)
            progress += 1
        worthWhile = APIFuntion.delDups(worthWhile)
        levels += 1

    window['-TASK-'].update("Checking Playtime:")
    progress = 0
    for id in worthWhile:
        progress_bar.UpdateBar(progress, len(worthWhile))
        outputTxt = str("Profile: " + str(id[0]) + " | " + str(progress + 1) + " Out Of " + str(len(worthWhile)))
        window['-OUTPUT-'].update(outputTxt)
        if not apiClass.hasPlayed(id[0]):
            dataList.append(id)
        progress += 1

    window['-TASK-'].update("Getting Information For Database:")

    progress = 0
    for i in dataList:
        progress_bar.UpdateBar(progress, len(dataList))
        outputTxt = str(str(progress + 1) + " Out Of " + str(len(dataList)))
        window['-OUTPUT-'].update(outputTxt)
        urlList.append(i[0])
        progress = + 1

    progress = 0
    returnList = []
    while len(urlList) > 100:
        progress_bar.UpdateBar(progress, (len(urlList) / 100) + 1)
        outputTxt = str(str(progress + 1) + " Out Of " + str((len(urlList) / 100) + 1))
        window['-OUTPUT-'].update(outputTxt)
        tempList = urlList[:100]
        urlList = urlList[100:]
        returnList = returnList + apiClass.getProfUrl(tempList)
        progress += 1
    returnList = returnList + apiClass.getProfUrl(urlList)

    returnList.sort()
    dataList.sort()

    progress_bar.UpdateBar((len(urlList) / 100) + 1, (len(urlList) / 100) + 1)

    count = 0
    for i in dataList:
        progress_bar.UpdateBar(count, len(dataList))
        outputTxt = str(str(count + 1) + " Out Of " + str(len(dataList)))
        window['-OUTPUT-'].update(outputTxt)
        i.append(returnList[count][1])
        count += 1

    window['-TASK-'].update("Adding Information to Database:")
    window['-OUTPUT-'].update("adding...")
    progress_bar.UpdateBar(0, 1)

    # change path
    accessDB = DataBase.AccessDB("SteamDB.accdb")
    accessDB.insetInto(dataList, 'STable1')
    accessDB.close()

    progress_bar.UpdateBar(1, 1)
    window['-TASK-'].update("Done")
    window['-OUTPUT-'].update("Done ")

    layout = [
        [sg.Text("Done!", size=(40, 1))],
        [sg.ProgressBar(1, orientation='h', size=(35, 20), key='progress')],
        [sg.Text("Would you like to go again", size=(40, 1))],
        [sg.Button('Continue'), sg.Quit()]
    ]

    window = sg.Window('TF2 Backpack Finder', layout).Finalize()
    progress_bar = window.FindElement('progress')
    progress_bar.UpdateBar(1, 1)
    event, values = window.read()

    if event == 'Quit':
        run = False
    