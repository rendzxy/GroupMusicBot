from os import path

from pyrogram import Client, filters
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch


import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Judul: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Durasi: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630),
        f"Request By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(
    filters.command(["play", "req", "putar"])
    & filters.group
    & ~ filters.edited
)
@errors
async def play(_, message: Message):

    lel = await message.reply("🔄 **Memproses** permintaanmu...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📢 Channel",
                        url="https://t.me/AnnabelleUpdates")
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Maaf! Lagu yang berdurasi lebih lama dari **{DURATION_LIMIT} menit** tidak dapat diputar,\nkarena durasi lagu yang kamu minta **{audio.duration / 60} menit**!"
            )

        thumbnail = thumb_name
        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📢 Channel",
                        url="https://t.me/AnnabelleUpdates")

                    ]
                ]
            )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
           # url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🎬 Lihat Di YouTube",
                                url=f"{url}")

                        ]
                    ]
                )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/638c20c44ca418c8b2178.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🎬 Lihat Di YouTube",
                                url=f"https://youtube.com")

                        ]
                    ]
                )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        await lel.edit("🔎 **Mencari** lagu yang kamu minta...")
        sender_id = message.from_user.id
        user_id = message.from_user.id
        sender_name = message.from_user.first_name
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

        query = ''
        for i in message.command[1:]:
            query += ' ' + str(i)
        print(query)
        await lel.edit("🔄 **Memproses** permintaanmu...")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            lel.edit(
                "❎ **Lagu tidak ditemukan**.\nCoba lagu lain atau mungkin tulis nama lagu dengan benar!"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎬 Lihat Di YouTube",
                            url=f"{url}")

                    ]
                ]
            )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=thumb_name, 
        caption=f"#⃣ Lagu yang kamu minta ditambah ke **antrian nomer {position}**.",
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo=thumb_name,
        reply_markup=keyboard,
        caption="▶️ **Memutar lagu** request by {} via YouTube.".format(
        message.from_user.mention()
        ),
    )
        os.remove("final.png")
        return await lel.delete()
