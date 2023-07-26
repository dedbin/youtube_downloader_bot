
from moviepy.editor import VideoFileClip, AudioFileClip


def merge_video_audio(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    video = video.set_audio(audio)
    video.write_videofile(output_file)



video_file = r'C:\Users\red1c\youtube_downloader\video\825204352_2023-07-26_12-51-06.mp4'
audio_file = r'C:\Users\red1c\youtube_downloader\video\825204352_2023-07-26_12-51-06.mp3'
output_file = r'merged_video.mp4'

merge_video_audio(video_file, audio_file, output_file)

def removeDuplicatesfromarray(arr):
    newArr = []
    for i in arr:
        if i not in newArr:
            newArr.append(i)
    return newArr

print(removeDuplicatesfromarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))