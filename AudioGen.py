from Utils import * 
from TTS import *
from VideoUtils import *
import nodriver as uc
from KreaArt import fetchArt
import os
from postVid import postYT, setPost
from TikTokUploader import upload_tiktok

pause_length = 0.5
max_chars_per_line = 80

def main():    
    Book = "Genisis"
    chapter, start_line = log()
    max_words = 70
    max_chars_per_images = 399
    lines, lineNumber = findHowManyLines(Book, chapter, start_line, max_words)
    text = " ".join(lines)
    num_lines = len(lines)

    path = "Generated/Final/Genisis 1:[1-5].mp4"
    print(f"Text: \n \n {text} \n \n")
    
    title = f"{Book} {chapter}:[{start_line}-{start_line+len(lines)}]"
    print("Posting to YT shorts...")
    setPost()
    try:
        postYT(path, title + " Creation", text)
        print(f"{path} published to YT shorts")
    except: 
        print("video could not be uploated to YT shorts, check quota and try again tomorrow")
    print("Posting to TikTok...")
    #upload_tiktok(video=path, description=text, accountname="mcblender0", hashtags=['God', '#Jeasus'])

    try:
       # upload_tiktok(path, description=text, accountname="mcblender0", hashtags=['God', '#Jeasus'])
        print(f"{path} published to TikTok")
    except: 
        print("viedo could not be uploated to TikTok")

    



if __name__ == "__main__":
    main()