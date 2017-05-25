"""
Tool to keep yourself aware of recent crypto events.

Made by Arttu Mahlakaarto,
"""

from contextlib import contextmanager
import sys
import os
import time
from datetime import datetime
outp=""
"""Edit only these 2 lines."""
ZEC = {'name': 'ZEC', 'value': 0, 'oldValue': 0, 'difference': 0, 'color': 'white', 'currency': 'BTC'}
ETH = {'name': 'ETH', 'value': 0, 'oldValue': 0, 'difference': 0, 'color': 'white', 'currency': 'BTC'}
XMR = {'name': 'XMR', 'value': 0, 'oldValue': 0, 'difference': 0, 'color': 'white', 'currency': 'BTC'}
BTC = {'name': 'BTC', 'value': 0, 'oldValue': 0, 'difference': 0, 'color': 'white', 'currency': 'USD'}
"""Dont edit anything below"""

worth = [0]
difference = [0]
def generateSpeech(text, filename):
    """Generate the mp3 File using google api."""
    from gtts import gTTS
    tts = gTTS(text=text, lang='en-us', slow=False)
    tts.save(filename+".mp3")
    return


def getCoin(coin, cu):
    """Get Value of coin in currency (cu)."""
    import requests
    re = "https://min-api.cryptocompare.com/data/price?fsym="+coin+"&tsyms="+cu
    response = requests.get(re)
    output = format(response.json()[cu])
    return(output)


@contextmanager
def suppress_stdout():
    """Silence the whining."""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def playSound(path):
    """Play the soundfile."""
    import time
    import vlc
    from mutagen.mp3 import MP3
    with suppress_stdout():
        audio = MP3(path)
        length = audio.info.length
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(path)
        player.set_media(media)
        player.play()
    time.sleep(length)

    return


def colorize(dict):
    """Return Colorized string."""
    dif = dict['difference']
    if(dif < 0.0000000000000000):
        dict['color'] = "red"
    if(dif > 0.00000000000000):
        dict['color'] = "green"
    if(dif == 0.000000000000000):
        dict['color'] = "white"



def generateStringsPure(dict):

    outpure = dict['name']+". value: "+str(dict['value']).replace('.',' point ')+" . change: "+str(dict['difference']).replace('.',' point ')+ " . "

    return(outpure)
def generateStrings(dict):
    from termcolor import colored
    outp = dict['name']+": "+str(dict['value']).replace('.',',')+" . "+colored(str(dict['difference']), dict['color'])+ " | "

    return(outp)


# strings = str("{:.5f}".format(difference[x]))

def clearScreen():
    """Check os and clear the screen."""
    import platform
    import os
    osystem = platform.system()

    if(osystem == "Windows"):
        os.system('cls')
    if(osystem == "Linux" or osystem == "Darwin" ):
        os.system('clear')
    return


def checkDifference(dict):
    """Check Difference between old and new."""
    dict['difference']=round(float(dict['value'])-float(dict['oldValue']),6)
    colorize(dict)
    dict['oldValue'] = dict['value']
    return

def checkValue(dict):
    """Check value of all coins in list"""
    dict['value']=round(float(getCoin(dict['name'],dict['currency'])),5)
    checkDifference(dict)
    return


while True:
# Loop
    checkValue(ZEC)
    pri = generateStrings(ZEC)
    checkValue(ETH)
    pri+=generateStrings(ETH)
    checkValue(BTC)
    pri+=generateStrings(BTC)
    pure=generateStringsPure(ZEC)
    pure+=generateStringsPure(ETH)
    pure+=generateStringsPure(BTC)


    clearScreen()
    print("")
    print("-----------------------------------------------------------------------------------------------------")
    print(pri)
    print("-----------------------------------------------------------------------------------------------------")
    #generateSpeech(pure, "forecast")
    #playSound("forecast.mp3")
    time.sleep(5)
