#/usr/bin/python3

# https://github.com/home-assistant-libs/pychromecast/blob/master/examples/youtube_example.py

import time
import urllib.request
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

destination = "Office"
chromecasts = None
browser = None

def main():

  chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[destination])
  
  while True: # main loop

    if not chromecasts:
      print("No Chromecast with that name found")
      time.sleep(10)
      restartDiscovery()
      continue

    try:
      cast = chromecasts[0]
      cast.wait()
      yt = YouTubeController()
      cast.register_handler(yt)
    except:
      print("No Chromecast with that name found")
      restartDiscovery()
      continue

    try:

      tagid = input("NFC Tag ID: ") # user input
      if tagid == "": # if the user just presses enter
        tagid = "00BAF91F04" # for testing

      print(cast.status)

      yt.clear_playlist()
      
      correspondingid = urllib.request.urlopen("https://script.google.com/macros/s/AKfycbw9KcSfkivP_ZJG53Ix-2fr-Vkk63KZK7Wfsj10hkNvAOu2XddJy8xjVJSOO4HZKqk3/exec?id=" + tagid).read().decode("utf-8")
      correspondingid = correspondingid.replace("https://youtu.be/", "").replace("https://www.youtube.com/watch?v=", "").replace("https://music.youtube.com/watch?v=", "")

      try:
        yt.play_video(correspondingid)
      except:
        print("Problem playing video")
        continue

      if cast.status.volume_level <= .3:
        try:
          cast.set_volume(.3)
        except:
          print("Problem setting volume")

    except KeyboardInterrupt:
      print("Stopping...")
      chromecasts[0].quit_app()
      browser.stop_discovery()
      break

    except:
      print("Error")
      chromecasts[0].quit_app()
      browser.stop_discovery()
      continue

def restartDiscovery():
  pychromecast.discovery.stop_discovery(browser)
  chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[destination])

if __name__ == '__main__':
  main()
