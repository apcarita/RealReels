
import os
import random
from datetime import datetime
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.video.fx.crop as crop_vid
from moviepy.editor import TextClip, CompositeVideoClip
import pysrt

# Take in audio and an array of images (paths) and then stitch them all together to create 1 video
def stitch(audio_path, images, output_path, number_of_lines, background_music, pause_length):
    # Sort images to ensure they are in order
    images.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1]))

    audio = AudioFileClip(audio_path)
    if audio.duration >= 59:
        print("WARNING VIDEO IS LONGER THAN 59 SECONDS")
    clips = []
    for image_path in images:
        img_clip = ImageClip(image_path).set_duration((audio.duration + number_of_lines*pause_length) / len(images))
        clips.append(img_clip)
    # Add background music
    

    background_music = AudioFileClip(background_music)

    random_time = random.uniform(0, background_music.duration - audio.duration)
    background_music = background_music.subclip(random_time, random_time + audio.duration)

    final_audio = CompositeAudioClip([audio, background_music.volumex(0.36)])  # Adjust volume as needed

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(final_audio)
    video.write_videofile(output_path, codec='libx264', fps=24)
   


    return output_path
# Take in video, and SRT then save a video with subtitels added to outputpath
def addSubtitles(video_path, srt_path, output_path, max_chars_per_line):
    video = VideoFileClip(video_path)
    subtitles = pysrt.open(srt_path)
    subtitle_clips = []

    line = ""
    last_end_time = 0
    for subtitle in subtitles:
        start_time = subtitle.start.hours * 3600 + subtitle.start.minutes * 60 + subtitle.start.seconds + subtitle.start.milliseconds / 1000
        end_time = subtitle.end.hours * 3600 + subtitle.end.minutes * 60 + subtitle.end.seconds + subtitle.end.milliseconds / 1000

        line = line + " " + subtitle.text

        if len(line) > max_chars_per_line or line == "":
            line = "\"" + subtitle.text
        
        if(len(line) > 3):
            add = "\""
        else: add = ""
        font = 'October-Condensed-Devanagari-Heavy'
        font = 'Big-Caslon-Medium'
        next_start_time = subtitles[subtitles.index(subtitle) + 1].start.hours * 3600 + subtitles[subtitles.index(subtitle) + 1].start.minutes * 60 + subtitles[subtitles.index(subtitle) + 1].start.seconds + subtitles[subtitles.index(subtitle) + 1].start.milliseconds / 1000 if subtitles.index(subtitle) + 1 < len(subtitles) else video.duration
        text_clip = TextClip(line + add, fontsize=88, font='Big-Caslon-Medium', color='White', bg_color='none', size=(video.size[0]*11/12, video.size[1]*2/6), method='caption', align='north')
        text_clip = text_clip.set_start(start_time).set_duration(next_start_time - start_time)

        print(f"adding subtitle {line} {last_end_time} to {next_start_time}")
        last_end_time = end_time
        text_clip = text_clip.set_position(('center', 'center'))

        subtitle_clips.append(text_clip)

    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_path, codec='libx264', remove_temp=True, fps = 30)
    

    return output_path

def testimages():
    image_folder = 'Generated/temp'
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    return image_paths

if __name__ == "__main__":
    print(testimages())
    print(TextClip.list('font'))
