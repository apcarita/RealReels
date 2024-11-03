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
    Religion()

def Smut():
    Book = "Court of Thorns"



def Religion():    
    Book = "Genisis"
    chapter, start_line = log()
    max_words = 95
    max_chars_per_images = 399
    lines, lastLineNumber, nchapter = findHowManyLines(Book, chapter, start_line, max_words)
    text = " ".join(lines)
    num_lines = len(lines)

    print(f"Text: \n \n {text} \n \n")
    
    title = f"{Book} {nchapter}:[{start_line}-{lastLineNumber}]"
    #images = testimages()
    images = uc.loop().run_until_complete(fetchArt(describe(text), 7, f"Generated/images/{title}"))

    audio_path = f"Generated/Audio/Complete/{title}.mp3"
    if not os.path.exists(audio_path):
        audio = makeAudio(lines, audio_path, pause_length)
    else:
        audio = audio_path
        print("already exists, not generating new audio")

    srt_path = f"Generated/srt/{title}.srt"
    srt = transcribe(audio, srt_path)

    planeVideo = stitch(audio, images, f"Generated/Intermediate/{title}.mp4", num_lines, "Cathedral_music.mp3")
    print(f"stitched video and saved to: {planeVideo}")

    finalVideo = addSubtitles(planeVideo, srt, f"Generated/Final/{title}.mp4")
    #finalVideo = addSubtitles(srt, f"Generated/Final/{title}.mp4")

    logComplete(nchapter, start_line, lastLineNumber, finalVideo)

    input("Press Enter to upload...")

    print("Posting to YT shorts...")
    setPost()
    try:
        postYT(finalVideo, title, text)
        print(f"{finalVideo} published to YT shorts")
    except: 
        print("video could not be uploated to YT shorts, check quota and try again tomorrow")
    print("Posting to TikTok...")
    try:
        upload_tiktok(finalVideo, description=text, accountname="scrolls_for_jesus", hashtags=['#bible', '#God', '#Jesus', '#faith', '#scripture', '#Christianity', '#religion', '#spirituality'])
        print(f"{finalVideo} published to TikTok")
    except: 
        print("viedo could not be uploated to TikTok")

    
    



if __name__ == "__main__":
    main()