import os
import multiprocessing
from pytube import YouTube
from playsound import playsound

def main():

  if not os.path.exists("cache"):
    os.makedirs("cache")
  
  playing = None # the process that is currently playing music

  while True: # main loop

    request = input("YouTube URL or ID: ") # user input
    if request == "":
      request = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # for testing

    try:
      yt = YouTube(request) # try to get the video
    except:
      request = "https://www.youtube.com/watch?v=" + request # if it's not a URL
      yt = YouTube(request) # try to get the video with the ID
    
    print("Downloading...")
    downloadpath = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download("cache") # highest quality audio
    print("Downloaded!")

    if playing is not None:
      playing.terminate() # stop the current process

    playing = multiprocessing.Process(target=playsound, args=(downloadpath,)) # create a new process
    playing.start() # and start it

if __name__ == '__main__':
  main()