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
    hashtags = ['#faith', '#religion', '#spirituality', '#bible', '#god', '#jesus', '#christianity']
    CheckQueue("Genesis", hashtags)
    
    finalVideo, title, text = CreateReel("Genesis", 95,"Cathedral_music.mp3", 0 )

    input("Press Enter to Continue...")

    upload(finalVideo, title, text, hashtags)

def CreateReel(Book, max_words, music, book_layout = 1):    
    #Book = "Genisis"
    chapter, start_line = log(Book)
    #max_words = 95
    max_chars_per_images = 399
    if book_layout == 0:
        print("using bible layout")
        lines, lastLineNumber, nchapter = findHowManyLines(Book, chapter, start_line, max_words)
    else:
        lines, lastLineNumber, nchapter = findHowManyLinesBook(Book, chapter, start_line, max_words)
    text = " ".join(lines)
    num_lines = len(lines)

    print(f"Text: \n \n {text} \n \n")
    
    title = f"{Book} {nchapter}:[{start_line}-{lastLineNumber}]"
    #images = testimages()

    image_dir = f"Generated_{Book}/images/{title}"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        images = uc.loop().run_until_complete(fetchArt(describe(text), 7, image_dir))
    else: 
        images = [f"{image_dir}/{i}" for i in os.listdir(image_dir)]
        print("images already exist, not fetching new images")

    audio_dir = f"Generated_{Book}/Audio/Complete"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    audio_path = f"{audio_dir}/{title}.mp3"
    if not os.path.exists(audio_path):
        audio = makeAudio(lines, audio_path, pause_length)
    else:
        audio = audio_path
        print("already exists, not generating new audio")
    
    if not os.path.exists(f"Generated_{Book}/srt"):
        os.makedirs(f"Generated_{Book}/srt")

    srt_path = f"Generated_{Book}/srt/{title}.srt"
    srt = transcribe(audio, srt_path)
    
    intermediate_dir = f"Generated_{Book}/Intermediate"
    if not os.path.exists(intermediate_dir):
        os.makedirs(intermediate_dir)
    planeVideo = stitch(audio, images, f"{intermediate_dir}/{title}.mp4", num_lines, music)
    print(f"stitched video and saved to: {planeVideo}")

    final_dir = f"Generated_{Book}/Final"
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    finalVideo = addSubtitles(planeVideo, srt, f"{final_dir}/{title}.mp4")
    #finalVideo = addSubtitles(srt, f"Generated/Final/{title}.mp4")
    # def logComplete(book, chapter, text, startline, lastline, output_path):
    logComplete(Book, nchapter, text, start_line, lastLineNumber, finalVideo)

    return finalVideo, title, text

def upload(finalVideo, title, text, hashtags):
    print("Posting to YT shorts...")
    setPost()
    print(f"uploading {finalVideo} to YT shorts")
    try:
        postYT(finalVideo, title, " ".join(hashtags) + " " + text)
        print(f"{finalVideo} published to YT shorts")
    except: 
        print("video could not be uploated to YT shorts, check quota and try again tomorrow")
    print("Posting to TikTok...")
    try:
       # upload_tiktok(finalVideo, description=text, accountname="scrolls_for_jesus", hashtags=hashtags)
        print(f"{finalVideo} published to TikTok")
    except: 
        print("viedo could not be uploated to TikTok")
    RemoveUploadQueue("Genesis")

    
def CheckQueue(book, hashtags):
    print(f"Checking upload queue for {book}")
    array = uploadQueue(book)
    print(array)
    if(array != []):
        title, text, finalVideo  = array
        upload(finalVideo, title, text, hashtags)
        print("upload complete")
    else:
        print("no videos wating for upload")

if __name__ == "__main__":
    main()
