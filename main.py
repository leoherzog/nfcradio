#/usr/bin/python3

import os
import subprocess
import urllib.request
from pytube import YouTube
import vlc

def main():

  if not os.path.exists("cache"):
    os.makedirs("cache")
  
  playing = vlc.Instance() # the process that is currently playing music
  playing.media_player_new()

  while True: # main loop

    try:

      tagid = input("NFC Tag ID: ") # user input
      if tagid == "": # if the user just presses enter
        tagid = "00BAF91F04" # for testing
      
      correspondingid = urllib.request.urlopen("https://script.google.com/macros/s/AKfycbw9KcSfkivP_ZJG53Ix-2fr-Vkk63KZK7Wfsj10hkNvAOu2XddJy8xjVJSOO4HZKqk3/exec?id=" + tagid).read().decode("utf-8")

      try:
        yt = YouTube(correspondingid) # try to get the video
      except:
        correspondingid = "https://www.youtube.com/watch?v=" + correspondingid # if it's not a URL
        try:
          yt = YouTube(correspondingid) # try to get the video with the ID
        except:
          print("No ID found")
          continue

      playing.stop()
        
      print("Downloading...")
      downloadpath = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download("cache") # highest quality audio
      print("Downloaded!")
      
      print("Playing...")
      playing.set_media(downloadpath)
      playing.play() # and start it

    except KeyboardInterrupt:
      print("Stopping...")
      playing.stop()
      break

    except Exception as e:
      print("Error:" + str(e))
      playing.stop()
      continue

if __name__ == '__main__':
  main()