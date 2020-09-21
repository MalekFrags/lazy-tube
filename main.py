import multiprocessing 
from requests_functions import MainFile
from discordBot import sendMessage

#MAIN PROGRAM
if __name__ == '__main__':
    mainProgram = multiprocessing.Process(target=MainFile)
    sendingDiscordMessage = multiprocessing.Process(target=sendMessage)
    
    sendingDiscordMessage.start()
    mainProgram.start()

    sendingDiscordMessage.join()
    mainProgram.join()