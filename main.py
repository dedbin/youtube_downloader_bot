import os
from pytube import YouTube
import telebot
from telebot.async_telebot import AsyncTeleBot
import datetime
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip


def merge_video_audio(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    video = video.set_audio(audio)
    video.write_videofile(output_file)


TOKEN = '6426972757:AAEHB81By1ADGOoI41MToIgOk-U5UGZtKsI'
logfile = str(datetime.date.today()) + '.log'
YOUR_USER_ID = 825204352
mode = 'low_quality'
bot = AsyncTeleBot(TOKEN)

bot.set_my_commands([
        telebot.types.BotCommand("/start", "в самое начало"),
        telebot.types.BotCommand("/help", "а че делать"),
        telebot.types.BotCommand("/high_quality", "работает медленнее, но выше качество видео"),
        telebot.types.BotCommand("/low_quality", "работает быстрее, но ниже качество видео"),
    ])
@bot.message_handler(commands=['start'])
async def send_instructions(message):
    await bot.send_message(message.chat.id,
                           text=f"привет, {message.chat.username}! я бот для скачивания видео с YouTube. просто "
                                f"отправь мне ссылку на видео, а я загружу его и скину его тебе сюда. просто отправь "
                                f"мне ссылку, чтобы начать! у меня есть два режима 1. high_quality 2. low_quality. в "
                                f"первом режиме видео отправляется дольше, но качество выше, а во втором - дольше, "
                                f"но качество ниже. работают не все видео."
                                f"извини. ♥")


@bot.message_handler(commands=['help'])
async def send_instructions(message):
    await bot.send_message(message.chat.id,
                           "я бот для скачивания видео с YouTube. просто отправь мне ссылку на видео, а я загружу и "
                           "скину его тебе сюда.")

@bot.message_handler(commands=['low_quality'])
async def send_instructions(message):
    global mode
    mode = 'low_quality'
    print(f'{mode=}' + 'изменил качество видео на low')
    await bot.send_message(message.chat.id,
                           "изменил качество видео на low")

@bot.message_handler(commands=['high_quality', 'high_qulity'])
async def send_instructions(message):
    global mode
    mode = 'high_quality'
    print(f'{mode=}' + 'изменил качество видео на high')
    await bot.send_message(message.chat.id,
                           "изменил качество видео на high")


@bot.message_handler(content_types=['text'])
async def download_video(message):
    global mode
    try:
        yt = YouTube(message.text)
        mess_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f'{mode=}')
        if mode == 'high_quality':
            try:
                yt.streams.filter(abr='160kbps', progressive=False).first().download(
                    filename=f'{message.chat.id}_{mess_time}.mp3',
                    output_path='C:/Users/red1c'
                                '/youtube_downloader/video/',
                    )
                yt.streams.filter(res='1080p', progressive=False).first().download(
                    filename=f'{message.chat.id}_{mess_time}.mp4',
                    output_path='C:/Users/red1c'
                                '/youtube_downloader/video/',
                    )
                await bot.send_message(message.from_user.id, "начал загрузку видео")
                merge_video_audio(video_file=f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp4',
                                  audio_file=f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp3',
                                  output_file=f'C:/Users/red1c/youtube_downloader/video/finished_video_{message.chat.id}_{mess_time}.mp4')
                await bot.send_message(message.from_user.id, "закончил загрузку видео")
                #           C:\Users\red1c\youtube_downloader\video\finished_video_825204352        _2023-07-26_14-22-57.mp4
                with open(f'C:/Users/red1c/youtube_downloader/video/finished_video_{message.chat.id}_{mess_time}.mp4', 'rb') as video:
                    await bot.send_video(message.chat.id, video, caption=f"{yt.title} ")
                    os.remove(f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp4')
                    os.remove(f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp3')
                    os.remove(f'C:/Users/red1c/youtube_downloader/video/finished_video_{message.chat.id}_{mess_time}.mp4')
            except Exception as ex:
                await bot.send_message(message.from_user.id, "что-то пошло не так </3, кинь другой url пожалуйста")
                with open(logfile, 'a', encoding='utf-8') as file:
                    err = (str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(
                        message.from_user.id) + ':' + str(
                        message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(
                        message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(ex) + '\n')
                    file.write(err)
                await bot.send_message(YOUR_USER_ID, err)
        elif mode == 'low_quality':
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
                output_path='C:/Users/red1c/youtube_downloader/video/',
                filename=f'{message.chat.id}_{mess_time}.mp4',
                max_retries=3
            )
            with open(f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp4',
                      'rb') as video:
                await bot.send_video(message.chat.id, video, caption=f"{yt.title} ")
                os.remove(f'C:/Users/red1c/youtube_downloader/video/{message.chat.id}_{mess_time}.mp4')
    except Exception as ex:
        await bot.send_message(message.from_user.id, "что-то пошло не так </3, кинь другой url пожалуйста")
        with open(logfile, 'a', encoding='utf-8') as file:
            err = (str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(
                message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(
                message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(ex) + '\n')
            file.write(err)
        await bot.send_message(YOUR_USER_ID, err)


if __name__ == '__main__':
    try:
        asyncio.run(bot.polling(none_stop=True, interval=0))
    except Exception as e:
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + str(e) + '\n')
        bot.send_message(YOUR_USER_ID, str(datetime.datetime.today().strftime("%H:%M:%S")) + str(e))
