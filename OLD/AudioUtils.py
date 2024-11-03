import datetime
from pydub import AudioSegment
import assemblyai as aai
from dotenv import load_dotenv
import os
import pysrt

def log():
    current_time = datetime.datetime.now()

    # Write the current time to the log file

    with open("testLog", "r") as log_file:
        lines = log_file.readlines()
        chapter = int(lines[-1].strip()[-1]) + 1 if lines else 0  # Get the last line or None if the file is empty

    with open("log", "a") as log_file:
        print(f"Running at {current_time}...\n working on chapter: {chapter}")
        log_file.write(f"Script ran at: {current_time} | Generating Genisis {chapter}\n")
    return chapter

def getChapter(book, chapter):
    lines = []
    with open(book, "r") as file:
        for line in file:
            # Check if the line starts with '1'
            if line.strip().startswith(f"{chapter}:"):
                # Remove all digits and strip whitespace
                cleaned_line = ''.join(filter(lambda x: not x.isdigit(), line)).strip()[2:]
                lines.append(cleaned_line)
        text = ' '.join(lines)
    return lines, text

def expand(path, maxDur, lines):
    output_path_list = []

    audio_clip = AudioSegment.from_file(path) 
    duration = audio_clip.duration_seconds
    num_clips_to_split = int(duration//maxDur)+1
    print(f"Generating {num_clips_to_split} Vidoes...\n")

    #if(duration%num_clips_to_split < 8 & num_clips_to_split > 1):
       # num_clips_to_split+=1
    
    durEachClip = duration/num_clips_to_split
    end = 0
    for i in range(num_clips_to_split):
        
        tstart = end
        tend = start+durEachClip*1000
        temp_output_path = f"Generate/temp.mp3"
        print(f"Generating {temp_output_path} from {tstart} to {tend} with duration: {durEachClip}" )
        trimmed_audio_clip = audio_clip[tstart:tend]
        trimmed_audio_clip.export(temp_output_path, format="mp3")

        srt_path = transcirbe(temp_output_path, "Generated/temp.srt")
        subs = pysrt.open(srt_path)
        
        lastIndex = -999
        for k, subttl in enumerate(subs):
            index = -(k+1)
            txt = subs[index]
            if lastIndex != -999:
                if txt in lines[lastIndex]:
                    del subs[index]
                    continue
                else:
                    break

            if(txt >= 7):
                del subs[index]
                continue
            for j,words in enumerate(lines):
                if txt in words:
                    lastIndex = j
                    break
                else:
                    del subs[index]
            #resave srt
        subs.save(f"{srt_path}.{k}", encoding = 'utf-8')

        subtitle = subs[-1]
        las_sub_time = subtitle.end.hours * 3600 + subtitle.end.minutes * 60 + subtitle.end.seconds + subtitle.end.milliseconds / 1000
        
        start = end 
        end = start + las_sub_time * 1000
        output_path = f"{path[:-4]}.{i}.mp3"
        print(f"Generating {output_path} from {start} to {end} with duration: {durEachClip}" )
        trimmed_audio_clip = audio_clip[start:end]
        trimmed_audio_clip.export(output_path, format="mp3")
        output_path_list.append(output_path)

    return output_path_list, durEachClip, num_clips_to_split

def transcirbe(video_path, srt_output_path):
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_path)
    srt = transcript.export_subtitles_srt(c1hars_per_caption=15)
    with open(srt_output_path, "w") as f:
        f.write(srt)
    return srt_output_path


