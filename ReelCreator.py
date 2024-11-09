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
    #CheckQueue("Genesis", hashtags)
    finalVideo, title, text = CreateReel("Genesis", 95,"Cathedral_music.mp3", "Daniel")


    input("Do you want to upload this video? press Enter")
    upload(finalVideo, title, text, hashtags)

    #christmasHashTags = ['#Christmas', '#MerryChristmas', '#ChristmasEve', '#ChristmasTree', '#HolidaySeason', '#SantaClaus', '#Xmas']
    #finalVideo, title, text = CreateReel("Frosty", 95,"Frosty The Snowman (Instrumental).mp3", "1wg2wOjdEWKA7yQD8Kca")
   # upload(finalVideo, title, text, christmasHashTags)



def CreateReel(Book, max_words, music, voice):    
    #Book = "Genisis"
    chapter, start_line = log(Book)
    #max_words = 95
    max_chars_per_images = 399
    lines, lastLineNumber, nchapter = findHowManyLines(Book, chapter, start_line, max_words)
    text = " ".join(lines)
    num_lines = len(lines)

    print(f"Text: \n \n {text} \n \n")
    
    title = f"{Book} {nchapter}:[{start_line}-{lastLineNumber}]"
    #images = testimages()  
    safty = "Using less than 400 characters, describe the following text as a picture in less than 400 characters. for example:\n \" And the LORD said unto Cain, Where is Abel thy brother? And he said, I know not: Am I my brother's keeper? And he said, What hast thou done? the voice of thy brother's blood crieth unto me from the ground. And now art thou cursed from the earth, which hath opened her mouth to receive thy brother's blood from thy hand; : When thou tillest the ground, it shall not henceforth yield unto thee her strength; a fugitive and a vagabond shalt thou be in the earth. \n \" turns into: \n  \"a man stands alone in a desolate wasteland, with bood on his hands. a large authoritative figure stands above him, judging. His soul floats above his body in a stream of light as the being towering above him passes judgement.\" Mentaion people  Replace all nudity with something more apporiate (cover with leave ect.) Respond with only your description:"



    safty2 = "remove all the non-descirptive words, and make it more concise. Replace any nudity in the text with something more appropriate (cover with leaves ect.) and make sure the text describes what people are wearing before describing them (also remove the names Adam and Eve). Respond only with the revised text:"

    superSafty = "start by breifly describe the setting in a Family Friendly way. Avoid any describing characteristics that could alude to women (don't say lush and devine without first specifing what is lush and devine). then events and characters. When describing people alway describe thier outfit before them (ex: wearing a green dress, a women). Whenever somone is naked, say they are covered in before describing them. USE LESS THAN 400 characters"

    image_dir = f"Generated_{Book}/images/{title}"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        images = uc.loop().run_until_complete(fetchArt(describe(text, safty), 7, image_dir))
        if images is None:
            print("NSFW Content Detected... Fetchign new images w/ safer prompt") 
            images = uc.loop().run_until_complete(fetchArt(describe(text, superSafty), 7, image_dir))
            return
    else: 
        images = [f"{image_dir}/{i}" for i in os.listdir(image_dir)]
        print("images already exist, not fetching new images")

    audio_dir = f"Generated_{Book}/Audio/Complete"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    audio_path = f"{audio_dir}/{title}.mp3"
    if not os.path.exists(audio_path):
        audio = makeAudio(lines, audio_path, pause_length, voice)
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
    postYT(finalVideo, title, " ".join(hashtags) + " " + text)
    print(f"{finalVideo} published to YT shorts")
        #print("video could not be uploated to YT shorts, check quota and try again tomorrow")
    print("Posting to TikTok...")
       # upload_tiktok(finalVideo, description=text, accountname="scrolls_for_jesus", hashtags=hashtags)
    print(f"{finalVideo} published to TikTok") 
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
