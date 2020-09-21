import os
import time
import datetime
import googleapiclient.discovery
from discordBot import sendMessage
import multiprocessing


#Personal Delay
def delay(prob_time):
    if(prob_time == 0):
        time.sleep(2.5)
    else:
        time.sleep(prob_time)
      
#Time format for the AddLog function  
def getTimeFormat():
    usefull_time = str(time.localtime(time.time()))[str(time.localtime(time.time())).find('(') + 1 : str(time.localtime(time.time())).find(', tm_yday')]
    dict_days = {'0': 'Monday',
                '1': 'Tuesday',
                '2': 'Wednesday',
                '3': 'Thursday',
                '4': 'Friday',
                '5': 'Saturday',
                '6': 'Sunday'}
    usefull_time = usefull_time.split(', ')
    for element in usefull_time:
        if('tm_year' in element):
            year = int( element[element.find('=') + 1:] )
        if('tm_mon' in element):
            month = int( element[element.find('=') + 1:] )
        if('tm_mday' in element):
            day = int( element[element.find('=') + 1:] )
        if('tm_hour' in element):
            hour = int( element[element.find('=') + 1:] )
        if('tm_min' in element):
            mins = int( element[element.find('=') + 1:] )
        if('tm_sec' in element):
            secs = int( element[element.find('=') + 1:] )
        if('tm_wday' in element):
            day07 = int( element[element.find('=') + 1:] )
            day0 = dict_days.get(str(day07))
    dict_time = {'tm_year': str(year),
                'tm_mon': str(month),
                'tm_mday': str(day),
                'tm_hour': str(hour),
                'tm_min': str(mins),
                'tm_sec': str(secs),
                'tm_wday': day0}
    return '[   (' + str(dict_time.get('tm_year')) +'/' + str(dict_time.get('tm_mon')) +'/' + str(dict_time.get('tm_mday')) +') | '+ str(day0) + ', ' + str(dict_time.get('tm_hour')) + ':' + str(dict_time.get('tm_min')) + ':' + str(dict_time.get('tm_sec')) +'   ]'

#Write all Logs in the log file
def addLog(action):
    with open(Logs_Path, 'a') as fileLog:
        fileLog.write(str(getTimeFormat()) + '  >  ' + action + '\n')
        
    with open(Logs_Path, 'r') as fileLog:
        fileLogs = fileLog.readlines()
        
    with open(Logs_Path, 'w') as fullFile:
        fullFile.write('')
        
        for line in fileLogs:
            fullFile.write(line)

#Sends the condition to send the discord message
#Add the video Id in VideoLinks
def addVideoLink(videoId, channelId):
    if(videoId != ''):
        addLog('(type=FileManagementUI) Adding a Video...')
        with open(VideoID_ChannelID_Path, 'a') as fileLog:
            fileLog.write(videoId + ' "-"-" ' + channelId + '\n')
        addLog('(type=FileManagementUI) Added a Video')
        
        delay(2)
        
        addLog('(type=FileManagement, DiscordBot) Adding video link in "' + Discord_VideoID_Path + '"...')
        with open(Discord_VideoID_Path, 'w') as Discord_VideoLinks:
            Discord_VideoLinks.write(videoId + '|send=F')
        addLog('(type=FileManagement, DiscordBot) Added video link in "' + Discord_VideoID_Path + '"')
        
        delay(2)
        
        addLog('(type=FileManagement) Waiting for the bot confirmation...')
        with open(Discord_VideoID_Path, 'r') as filetempVideo:
            tempVideo = filetempVideo.readlines()[0]
        while(tempVideo[-1:] == 'F'):
            with open(Discord_VideoID_Path, 'r') as filetempVideo:
                tempVideo = filetempVideo.readlines()[0]
                delay(1)
        addLog('(type=FileManagement) The confirmation is accepted')
           
#get the API key from the data.txt file      
def getAPI(link):
    with open(link, 'r') as fileData:
        data = fileData.readlines(1)[0]
        api_key = data[data.find(':') + 2:]
        
    return api_key

#Get the API key + Time for the settings
def Base_Information(f_s):
    if(f_s == 'apiKey'):
        with open(Logs_Path, 'w') as fileLog:
            fileLog.write('')
        with open(VideoID_ChannelID_Path, 'w') as fileLog:
            fileLog.write('')
        addLog('(type=FileManagement) Getting API...')
        api_key = getAPI(Data_Path)
        addLog('(type=FileManagement) Got API')
        
        return api_key
    
    
    elif(f_s == 'time'):
        
        return datetime.datetime.utcnow().isoformat() + "Z"
        #return "2020-09-19T23:00:00.324259Z"
    
#Send the request for googleapiclient.discovery.build
def GoogleClientRequest(apiKey):
    addLog('(type=GoogleRequest) Sending a Request to "googleapiclient.discovery.build"...')
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = apiKey)
    time.sleep(5)
    addLog('(type=GoogleRequest) Request Accepted from "googleapiclient.discovery.build"')
    
    return youtube

#Getting informations updated in Data.txt for optimizations
def updatingData():
    
    addLog('(type=FileManagement) Writing "tempData.txt"...')
    with open(Data_Path, 'r') as dataFile:
        readableDataFile = dataFile.readlines()
        
    with open(TempData_Path, 'w') as dataTempFile:
        dataTempFile.write('')
        
    with open(TempData_Path, 'a') as dataTempFile:
        lineCounter = 1
        for line in readableDataFile:
            if(lineCounter <= 4):
                dataTempFile.write(line)
                
            if(line[:line.find('/')] == 'channel'):
                dataTempFile.write(line)
            elif(line[:line.find('/')] == 'user'):
                dataTempFile.write('channel/' + getChannelID( line[:line.find(',')], youtube) + line[line.find(','):])
            
            lineCounter += 1
    addLog('Writing complete "tempData.txt"')
    
    delay(1)
    
    addLog('Updating "Data.txt" for optimization...')
    with open(TempData_Path, 'r') as dataTempFile:
        tempFile = dataTempFile.readlines()
        
    with open(Data_Path, 'w') as dataFile:
        dataFile.write('')
        for line in tempFile:
            dataFile.writelines(line)
    addLog('Updating completed for "Data.txt"')
    
#open data file and get all channel links
def getChannelLinks(link):
    with open(link, 'r') as fileData:
        fullFile = fileData.readlines()
    counter = 0
    while(fullFile[counter] != 'CHANNELS_TO_FOLLOW: {channel link}, {type of videos}, #NAME_CHANNEL\n'):
        counter += 1
    listLinks = fullFile[counter + 1:]
    for i in range(len(listLinks)):
        listLinks[i] = listLinks[i][:listLinks[i].find(',')]
        
    return listLinks

#Get list of the channel IDS
def channelIds(youtube):
    addLog('(type=FileManagement) Getting Channel IDs...')
    listLinks = getChannelLinks(Data_Path)
    listChannelId = []
    for half_link in listLinks:
        listChannelId.append(getChannelID(half_link, youtube))
    updatingData()
    addLog('(type=FileManagement) Got all Channel IDs')
    
    return listChannelId

#Get channel - > channel ID
def getChannelID(half_link, youtube):
    if('channel/' in half_link):
        addLog('(type=FileManagement) Got Channel ID of ' + half_link[half_link.find('/') + 1:])
        return half_link[half_link.find('/') + 1:]
    elif('c/' in half_link) or ('user/' in half_link):
        delay(0)
        username = half_link[half_link.find('/') + 1:]
        addLog('(type=id) Getting a request of Channel ID of "' +  username + '" ...')
        delay(0)
        request = youtube.channels().list(
                                            part="id",
                                            forUsername=username
                                        )
        addLog('(type=id) Got a request of Channel ID of "' + username + '" ...')
        
        addLog('(type=id) Executing the Request of "youtube.activities" of [' + username +']...')
        delay(0)
        response = request.execute()
        delay(0)
        addLog('(type=snippet) Execution is done of [' + username +']')
        for items in response['items']:
            channelId = dict(items).get('id')
        addLog('Got Channel ID of ' + channelId)
    
        return channelId

#getting snippet about a channel
def getChannelResponse(channelID, times, youtube):
    delay(0)
    addLog('(type=snippet) Sending a Request to "youtube.activities" of [' + channelID +']...')
    delay(0)
    request = youtube.activities().list(part="snippet", channelId=channelID, publishedAfter=times)
    delay(0)
    addLog('(type=snippet) Request Accepted from "youtube.activities" of [' + channelID +']')

    addLog('(type=snippet) Executing the Request of "youtube.activities" of [' + channelID +']...')
    delay(0)
    response = dict(request.execute())
    delay(0)
    addLog('(type=snippet) Execution is done of [' + channelID +']')
    
    return response

#getting contentDetails about a channel
def getChannelResponseLink(channelID, times, youtube):
    addLog('(type=contentDetails) Sending a Request to "youtube.activities" of [' + channelID +']...')
    delay(0)
    request = youtube.activities().list(part="contentDetails", channelId=channelID, publishedAfter=times)
    delay(0)
    addLog('(type=contentDetails) Request Accepted from "youtube.activities" of [' + channelID +']')

    addLog('(type=contentDetails) Executing the Request of "youtube.activities" of [' + channelID +']...')
    delay(0)
    response = dict(request.execute())
    delay(0)
    addLog('(type=contentDetails) Execution is done of [' + channelID +']')
    
    return response 

#get Video ID 
#send discord condtion to send messege
def Video_Information(listChannelId, times, youtube):
    addLog('Checking started: Checking if any channel uploaded a video...')
    videoId = ''
    for channel_ID in listChannelId:
        delay(0)
        everything_response = getChannelResponseLink(channel_ID, times, youtube)
        for items in everything_response['items']:
            delay(0)
            addLog('(type=contentDetails, upload) Getting a Video ID of "' + channel_ID + '" ...')
            videoIds = str(dict(dict(items).get('contentDetails')).get('upload')).split("'")
            
            if(videoIds != ['None']):   
                videoId = videoIds[3]
                addLog('(type=contentDetails, upload) Got Video ID')
                delay(0)      
                addVideoLink(videoId, channel_ID)
    addLog('Checking is complete. Will check again after 250 Seconds...')

#get video id
def getVideoId():
    with open(Discord_VideoID_Path , 'r') as Discord_VideoLinks:
        fileLinks = Discord_VideoLinks.readlines()
    return fileLinks[0]

#Main file
def MainFile(): 
    apiKey = Base_Information('apiKey')
    youtube = GoogleClientRequest(apiKey)
    delay(5)
    #theTime = Base_Information('time')
    theTime = "2020-09-20T23:00:00.324259Z"
    addLog("TIME SET : " + theTime)
    while(True):
        listChannelId = channelIds(youtube)
        Video_Information(listChannelId, theTime, youtube)
        theTime = Base_Information('time')
        addLog("TIME SET : " + theTime)
        delay(250)
   
def getPathsFixed(relativePath):
    return str(os.getcwd()) + "\\" + relativePath
   
   
#NEEDED PATHS
Logs_Path = getPathsFixed("Output-Files\\logs.txt")
VideoID_ChannelID_Path = getPathsFixed("Output-Files\\VideoID-ChannelID.txt")
Discord_VideoID_Path = getPathsFixed("Temporary-Data\\Discord-VideoID.txt")
TempData_Path = getPathsFixed("Temporary-Data\\tempData.txt")
Data_Path = getPathsFixed("data.txt")

#NEEDED VARIABLES
apiKey = Base_Information('apiKey')
youtube = GoogleClientRequest(apiKey)