from pytube import YouTube

def main():
  yt = YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ') 
  print(yt.streams.filter(only_audio=True).order_by('abr').desc().first())

if __name__ == '__main__':
  main()
