from ReelCreator import *   
import os
import moviepy.editor as mp

def main():
    folder = "Generated_Genesis/Final"
    chapter = 1
    audio_dir = "Generated_Genesis/Audio/Complete"
    video_dir = "Generated_Genesis/Intermediate"
    
    audio_filenames = [f for f in os.listdir(audio_dir) if f.startswith(f"Genisis {chapter}:")]
    video_filenames = [f for f in os.listdir(video_dir) if f.startswith(f"Genisis {chapter}:")]
    
    print(f"Audio files found: {audio_filenames}")
    print(f"Video files found: {video_filenames}")
    
    audio_filenames.sort()
    video_filenames.sort()
    
    print(f"Sorted audio files: {audio_filenames}")
    print(f"Sorted video files: {video_filenames}")

    stitched_clips = []
    for audio_file, video_file in zip(audio_filenames, video_filenames):
        audio_path = os.path.join(audio_dir, audio_file)
        video_path = os.path.join(video_dir, video_file)
        
        print(f"Processing audio file: {audio_path}")
        print(f"Processing video file: {video_path}")
        
        video_clip = mp.VideoFileClip(video_path)
        audio_clip = mp.AudioFileClip(audio_path)
        stitched_clips.append(video_clip.set_audio(audio_clip))

    if stitched_clips:
        final_video = mp.concatenate_videoclips(stitched_clips)
        output_path = f"Generated_Genesis/Final/Genesis_{chapter}_complete.mp4"
        
        print(f"Writing final video to: {output_path}")
        
        final_video.write_videofile(output_path, codec='libx264', fps=24)

if __name__ == "__main__":
    main()
