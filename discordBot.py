import discord
from discord.ext import commands
from discord.ext import tasks
import time
import os

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

#Personal Delay
def delay(prob_time):
    if(prob_time == 0):
        time.sleep(2.5)
    else:
        time.sleep(prob_time)
 
#Write all Logs in the log file     
def addLog(action):
    with open(Logs_Path, 'a') as fileLog:
        fileLog.write(str(getTimeFormat()) + '  >  ' + action +'\n')
    with open(Logs_Path, 'r') as fileLog:
        fileLogs = fileLog.readlines()
    with open(Logs_Path, 'w') as fullFile:
        fullFile.write('')
        for line in fileLogs:
            fullFile.write(line)

def getPathsFixed(relativePath):
    return str(os.getcwd()) + "\\" + relativePath

#still have to update it
def sendMessage():
        client = commands.Bot(command_prefix = '!')
        #client = discord.Client()

        @client.event
        async def on_ready():
                await client.change_presence(activity = discord.Game(name='Do !help'))
        
                channel = client.get_channel(751368446112956426)
                with open(Discord_VideoID_Path, 'r') as filetempVideo:
                        tempVideo = filetempVideo.readlines()
                
                while(tempVideo == []):
                        with open(Discord_VideoID_Path, 'r') as filetempVideo:
                                tempVideo = filetempVideo.readlines()
                                
                tempVideo = tempVideo[0]
                while(True): 
                        while(tempVideo[-1:] == 'F'):          
                                #addLog('DISCORD BOT : Checking if sending message is available...')
                                channel = client.get_channel(751368446112956426)
                                await channel.send('https://www.youtube.com/watch?v=' + tempVideo[:tempVideo.find('|')])
                                
                                
                                #addLog('(type=DiscordBot) Checking is complete')
                                delay(1.5)
                                with open(Discord_VideoID_Path , 'w') as filetempVideo:
                                        filetempVideo.write(tempVideo[:tempVideo.find('|')] + '|send=T')
                                #addLog('DISCORD BOT : Sent Video Link to #annoncements')
                                
                                
                                delay(0)
                                await client.change_presence(activity = discord.Game(name='Do !help'))
                                with open(Discord_VideoID_Path, 'r') as filetempVideo:
                                        tempVideo = filetempVideo.readlines()[0]                  
                        while(tempVideo[-1:] != 'F'):   
                                with open(Discord_VideoID_Path, 'r') as filetempVideo:
                                        tempVideo = filetempVideo.readlines()
                                        while(tempVideo == []):
                                                with open(Discord_VideoID_Path, 'r') as filetempVideo:
                                                        tempVideo = filetempVideo.readlines()
                             
                                        tempVideo = tempVideo[0]
                        await client.change_presence(activity = discord.Game(name='Do !help'))
                        delay(5)
        client.run("NzU0NzI5NDc2NTAzNTAyOTUw.X14-mQ.zdsUz6H2xu_T3R8mXRsQfBcoOvc")
        
#NEEDED PATHS
Logs_Path = getPathsFixed("Output-Files\\logs.txt")
VideoID_ChannelID_Path = getPathsFixed("Output-Files\\VideoID-ChannelID.txt")
Discord_VideoID_Path = getPathsFixed("Temporary-Data\\Discord-VideoID.txt")
TempData_Path = getPathsFixed("Temporary-Data\\tempData.txt")
Data_Path = getPathsFixed("data.txt")
