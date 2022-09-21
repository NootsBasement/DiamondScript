import pathlib as plib
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
import os
import sys
import subprocess
import win32clipboard
import pytube
from pytube import YouTube
from requests_html import HTMLSession
import requests
import psutil
from collections import OrderedDict

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voice')
listener.dynamic_energy_threshold = 1000
listener.pause_threshold = 1

#Retrieves PID Number just in case for future use.
def GetPIDNumber():
    pid = os.getpid()
    print("PID Number:", pid)
    return pid

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk("Loading Script")
print("Loading...")

#Finds Home Directory
def FindHomeDir():
    try:
        home_directory = os.path.expanduser('~') #idk how it works it just does B)
        start = home_directory
        print("Home Directory Found, Home Directory: " + start)
        return start
    except:
        print("Home Directory can't be found!")
        exit()
HomeUserDirectory = FindHomeDir()

#Finds Downloads Folder
def FindDownloadsFolder():
    for dirpath, dirnames, filenames in os.walk(HomeUserDirectory):
        for dirname in dirnames:
            if dirname == "Downloads":
                DownloadsScriptPath = os.path.join(dirpath, dirname)
                DownloadsScriptPathCreated = True
                if DownloadsScriptPathCreated == True:
                    print("Downloads Path Found")
    return DownloadsScriptPath
DownloadsFolderPath = FindDownloadsFolder()

#Main folder path containing all files
DiamondScriptFolderPath = DownloadsFolderPath + "\MainDiamondScript"
#MediaStorage path
MediaStoragePath = DiamondScriptFolderPath + "\MediaStorage"
#SoftwareShortcuts path
SoftwareShortcutsPath = DiamondScriptFolderPath + "\SoftwareShortcuts"

print("done loading script, script ready.")
print('say out loud, "diamond help" to receive all command phrases and functions that come with the script.')

#Listens and Processes the Command Given.
def take_command():
    command = None
    try:
        with sr.Microphone() as source:
            print('listening...')
            #timeout and phrase limit work together to fix bug where it listens forever (so far anyway)
            voice = listener.listen(source, timeout=3, phrase_time_limit=10)
            print("I finished listening.")
            #sends what was heard through googles speech api
            command = listener.recognize_google(voice)
            #response comes back lowercase
            command = command.lower()
    except:
        print(command)
        print("Nothing was heard.")
        pass
    return command


def run_diamond():
    command = take_command()
    if not command:
        return None
    print(command)

    def WipeTextBeforeCommand(text):
        def Convert(string):
            li = list(string.split(" "))
            return li

        definecommand = (Convert(command))

        for item in definecommand[:]:
            definecommand.pop(0)
            if 'diamond' in item:
                break

        convertlistbacktostr = ' '.join(definecommand)

        return convertlistbacktostr

    corrected_command = "diamond " + WipeTextBeforeCommand(command)
    print(corrected_command)
    #Search Youtube Command
    if 'diamond' in command:

        # AI response
        Youtube_Respone = 'I heard you and will now play requested video on youtube'

        # takes song requested and searches on youtube using pywhatkit
        def SearchYoutube():
            pywhatkit.playonyt(song)
            print(song)
            talk(Youtube_Respone)

        search_keywords = ['diamond search on youtube ',
                           'diamond search up on youtube ',
                           'diamond look up on youtube ',
                           'diamond search up on youtube ',
                           'diamond play on youtube ',
                           'diamond find on youtube ',
                           'diamond find the song on youtube named ',
                           'diamond play ']

        for search in search_keywords:
            if search in corrected_command:
                song = corrected_command.replace(search, '')
                SearchYoutube()

    # Time Commands
    if 'diamond' in command:

        def ExplainTime():
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk('Current time is ' + time)

        time_keywords = ['diamond what is the time',
                         "diamond what's the time",
                         'diamond what time is it']

        for keyword in time_keywords:
            if keyword in corrected_command:
                ExplainTime()

    #Microphone Testing Commands
    if 'diamond' in command:

        def MicrophoneTestResponse():
            print("Heard you.")
            talk('Microphone was heard, listening again')

        microphone_keywords = ['diamond test for microphone input',
                               'diamond this is a microphone test',
                               'diamond testing microphone',
                               'diamond testing for microphone input',
                               'diamond can i be heard',
                               'diamond can you hear me',
                               'diamond are you there']

        for keyword in microphone_keywords:
            if keyword in corrected_command:
                MicrophoneTestResponse()

    #Diamond's Generic Responses
    if 'diamond' in command:

        generic_keyword = ['diamond how are you',
                           'diamond how are you doing',
                           'diamond nae nae']

        for keyword in generic_keyword:
            if keyword in corrected_command:
                print("Heard you.")
                talk("I'm fine")

    #Web Search Cmds
    if 'diamond' in command:
        if 'diamond search ' in corrected_command:
            search = corrected_command.replace('diamond search ', '')
            pywhatkit.search(search)
            talk("Searching")

    #System Commands
    if 'diamond' in command:

        #Shuts down Pc
        if 'diamond turn off my computer' in corrected_command:
            talk("Shutting Down in 10 Seconds")
            import time
            time.sleep(10)
            subprocess.call("shutdown /s")
        #Restarts PC
        if 'diamond restart my computer' in corrected_command:
            talk("Shutting Down in 10 Seconds")
            import time
            time.sleep(10)
            subprocess.call("shutdown /r")

    #Youtube Commands
    if 'diamond' in command:

        def ExtractClipboardData():
            win32clipboard.OpenClipboard()
            link = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return link

        if 'diamond convert youtube to video' in corrected_command:
            link = ExtractClipboardData()
            print("Attempting to download link")
            talk("Attempting to download link")
            try:
                yt = YouTube(link)
                savedir = (MediaStoragePath)
                stream = yt.streams.get_highest_resolution()
                stream.download(savedir)
                talk("Downloaded Video")
                print("Downloaded Video")
            except:
                print("Copy A Youtube Link!")
                talk("ERROR Youtube link needs to be copied to clipboard for download")
                pass

        elif 'diamond convert youtube to audio' in corrected_command:
            link = ExtractClipboardData()
            talk("Attempting to download link")
            print("Attempting to download link")
            try:
                yt = YouTube(link)
                savedir = (MediaStoragePath)
                stream = yt.streams.get_audio_only()

                def GetPythonUserAgentVersion():
                    #Gets the current requests package version for user agent
                    requestsvers = (requests.__version__)
                    requestnameandvers = 'python-requests/' + requestsvers
                    soupconvertdict = {'User-Agent': requestnameandvers}
                    return (dict(soupconvertdict))

                UserAgent = GetPythonUserAgentVersion()
                Session = HTMLSession()
                url = (link)
                Request = Session.get(url, headers=UserAgent)
                VideoName = (Request.html.find('title', first=True).text)

                def IllegalCharacterRemover(VideoName):
                    illegalchar = ['@', '$', '%', '&', '\\', '/', ':', '*', '?', '"', "'", '<', '>', '|', '~', '`', '#',
                                   '^', '+', '=', '{', '}', '[', ']', ';', '!', ':']

                    def Convert(VideoName):
                        VideoList = []
                        VideoList[:0] = VideoName
                        return VideoList

                    ListedVideoName = Convert(VideoName)
                    removeillegalchar = [value for value in ListedVideoName if value not in illegalchar]
                    StringVideoName = ''.join(removeillegalchar)
                    return StringVideoName

                print(IllegalCharacterRemover(VideoName))
                FixedVideoName = IllegalCharacterRemover(VideoName)
                FinalVidName = FixedVideoName + ".mp3"
                print(FinalVidName)
                stream.download(savedir, filename=FinalVidName)
                talk("Downloaded Video")
                print("Downloaded Video")
            except:
                print("Copy A Youtube Link!")
                talk("ERROR Youtube link needs to be copied to clipboard for download")
                pass

        elif 'diamond convert youtube to bad video' in corrected_command:
            link = ExtractClipboardData()
            print("Attempting to download link")
            try:
                yt = YouTube(link)
                savedir = (MediaStoragePath)
                stream = yt.streams.get_lowest_resolution()
                stream.download(savedir)
                talk("Downloaded Video")
                print("Downloaded Video")
            except:
                print("Copy A Youtube Link!")
                pass

    #Opening Created Program Commands
    if 'diamond' in command:

        def ExtractClipboardData():
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data

        if 'diamond save program as ' in corrected_command:
            try:
                program_name = corrected_command.replace('diamond save program as ', '')
                ProgramFileName = SoftwareShortcutsPath + "\\" + program_name + ".bat"
                runcommand = 'break>' + '"' + ProgramFileName + '"'
                os.system(runcommand)
                path = '"' + ExtractClipboardData() + '"'
                with open(os.open(ProgramFileName, os.O_CREAT | os.O_WRONLY, 0o777), mode="w+") as InstructionsFile:
                    InstructionsFile.write(path)
                print("Program has been saved")
                talk("Program has been saved")
            except:
                print("Program couldn't be saved, copy the complete path to clipboard with file name and extension before saying command again!")
                talk("Program couldn't be saved, copy the complete path to clipboard with file name and extension before saying command again!")
                pass

        if 'diamond open ' in corrected_command:
            program_filename = corrected_command.replace('diamond open ', '')
            fileextensionname = program_filename + ".bat"
            for dirpath, dirnames, filenames in os.walk(SoftwareShortcutsPath):
                for filename in filenames:
                    if filename == fileextensionname:
                        programdirpath = os.path.join(dirpath, filename)
                        os.startfile(programdirpath)

    #Help Commands
    if 'diamond' in command:
        if 'diamond help' in command:
            print("Opening help file.")
            talk("opening help file.")
            HelpFilePath = DiamondScriptFolderPath + "\\DiamondCommands.txt"
            os.startfile(HelpFilePath)

    #Exit Commands
    if 'diamond' in command:
        if 'diamond stop script' in command:
            print("Stopped Script!")
            talk("Stopping Script")
            exit()

        elif 'diamond shut off' in command:
            print("Stopped Script!")
            talk("Stopping Script")
            exit()


    else:
        print("'I heard you, but I don't recognize the command'")


while True:
    run_diamond()