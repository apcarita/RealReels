from ReelCreator import *   
def main():
    hashtags = ['#faith', '#religion', '#spirituality', '#bible', '#god', '#jesus', '#christianity']
    #CheckQueue("Genesis", hashtags)
    CheckQueue("Genesis", hashtags)


    finalVideo, title, text = CreateReel("", "Genesis", 95,"Cathedral_music.mp3", "Daniel")
    upload(finalVideo, title, text, hashtags)


if __name__ == "__main__":
    main()
