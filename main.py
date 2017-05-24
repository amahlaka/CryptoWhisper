"""
Tool to keep yourself aware of recent crypto events.

Made by Arttu Mahlakaarto,
"""

oldZec = zecP = oldBtc = btcP = oldXmr = xmrP = oldEth = ethP = 0


def generateSpeech(text, filename):
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


from contextlib import contextmanager
import sys, os


@contextmanager
def suppress_stdout():
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

def getDifference(old, new):
    if(old == new):
        return(0.000)
    else:
        difference = float(new)-float(old)
        if(difference >= 0.5):
            generateSpeech("DIFFERENCE OVER 0.5!", "warning")
            playSound("warning.mp3")
        return(difference)


def colorize(inp):
    from termcolor import colored
    if(inp > 0):
        color = "green"
    if(inp < 0):
        color = "red"
    if(inp == 0):
        color = "grey"
    strings = str("{:.5f}".format(inp))
    colorizedString = colored(strings, color)
    return(colorizedString)
import time
from datetime import datetime
while True:

    zecP = getCoin("ZEC", "BTC")
    btcP = getCoin("BTC", "USD")
    xmrP = getCoin("XMR", "BTC")
    ethP = getCoin("ETH", "BTC")
    sp = "ZEC: "+zecP+". ETH: "+ethP+". XMR: "+xmrP+". BTC: "+btcP
    zecDiff = getDifference(oldZec, zecP)
    btcDiff = getDifference(oldBtc, btcP)
    xmrDiff = getDifference(oldZec, xmrP)
    ethDiff = getDifference(oldEth, ethP)
    spacer = "     "
    spacerb = "      "

    zc = colorize(zecDiff)
    bc = colorize(btcDiff)
    xc = colorize(xmrDiff)
    ec = colorize(ethDiff)
    oldZec = zecP
    oldBtc = btcP
    oldXmr = xmrP
    oldEth = ethP
    td = spacer+zc+spacerb+ec+spacerb+xc+spacerb+bc
    print("-------------------------------------------------------------------")
    print(sp+"  "+str(datetime.now().strftime('%H:%M:%S')))
    print(td)
    print("-------------------------------------------------------------------")
    generateSpeech(sp, "forecast")
    with suppress_output():
     playSound("forecast.mp3")

    time.sleep(5)
