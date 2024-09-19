from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop, resize
import os, datetime

def check_if_yes(string : str):
    if string.lower() in {'y', 'д', 'да', 'yes'}:
        return True
    return False

def time_str_to_sec(time_str : str):
    timestamp = datetime.datetime.strptime(time_str.split(',')[0],'%H:%M:%S')
    return datetime.timedelta(hours=timestamp.hour,minutes=timestamp.minute,seconds=timestamp.second).total_seconds()

def split_video(input_video, output_folder, start_time, end_time, can_make_short, segment_duration=30):
    clip = VideoFileClip(input_video)
    
    # Cut the video (start_time, end_time) with flooring
    clip = clip.subclip(start_time, end_time)

    # crop video
    cropped_clip = crop(clip, x_center=clip.w // 2, y_center=clip.h // 2, height=clip.h, width=int(clip.h // clip.aspect.ratio) if int(clip.h // clip.aspect_ratio) % 2 == 0 else int(clip.h // clip.aspect_ratio) + 1)
    clip = cropped_clip
    
    total_duration = clip.duration
    current_time = 0
    segment_number = len(next(os.walk(output_folder))[2]) + 1 if len(next(os.walk(output_folder))[2]) != 0 else 1
    
    while current_time < total_duration:
        # Cut fragment
        subclip_end_time = min(current_time + segment_duration, total_duration)
        subclip = clip.subclip(current_time, subclip_end_time)

        if(subclip_end_time - current_time < 30 and can_make_short == False): break
        
        # Save fragment
        output_path = f"{output_folder}/{os.path.basename(input_video)}segment_{segment_number}.mp4"
        subclip.write_videofile(output_path, codec="libx264")
        
        # Update timestamps
        current_time += segment_duration
        segment_number += 1

    # Close vid
    clip.close()

if __name__ == '__main__':
    input_video_path = input("Исходное видео: ")
    output_folder_path = "E:\Видео\Shorts"
    start_time = time_str_to_sec(input("Начало (Час:Мин:Сек):"))
    end_time = time_str_to_sec(input("Конец (Час:Мин:Сек):"))
    can_make_short = check_if_yes(input("Создавать короткие фрагменты:"))

    if end_time < start_time:
        print("Duration is negative")
        exit(0)
    
    confirm = input(f"Будет создано {int((end_time - start_time) // 30) + (1 if can_make_short else 0)} фрагментов. Подтвердить? [Д/Н]:")
    if check_if_yes(confirm):
        split_video(input_video_path, output_folder_path, start_time, end_time, can_make_short)
    exit(0)