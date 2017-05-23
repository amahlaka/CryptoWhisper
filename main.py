"""
Tool to keep yourself aware of recent crypto events.

Made by Arttu Mahlakaarto,
"""
coins = "ZEC"
def generateSpeech(text):
    from gtts import gTTS

    tts = gTTS(text=text, lang='en-us', slow=False)
    tts.save("test.mp3")
    return

def getCoin(coin, cu):
    """Get Value of coin in currency (cu)."""

    import requests
    re = "https://min-api.cryptocompare.com/data/price?fsym="+coin+"&tsyms="+cu
    response = requests.get(re)
    output = format(response.json()[cu])
    return(output)

def playSound(path):
    """Play the soundfile."""

    import time
    import vlc
    from mutagen.mp3 import MP3

    audio = MP3(path)
    length = audio.info.length
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(path)
    player.set_media(media)

    player.play()
    time.sleep(length)

    return

import time
coinvalue = getCoin(coins, "USD")
generateSpeech("Current value for "+coins+" is:"+coinvalue+" USD")
playSound("test.mp3")
time.sleep(1)
oldvalue = 250.3
while True:

    coinvalue = getCoin(coins, "USD")
    diffe = str(round(abs(float(coinvalue)-float(oldvalue)),3))
    generateSpeech(coins+" value: "+coinvalue+" USD, difference is: "+diffe)
    playSound("test.mp3")
    time.sleep(10)
    oldvalue = coinvalue
