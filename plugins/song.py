from __future__ import unicode_literals

import os
import requests
import asyncio
import math
import time
import wget
import re
import sys
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

youtube_regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

@Client.on_message(filters.private & filters.command("song"))
async def song(client, message):
    query = update.message.reply_to_message.text
    m = await update.message.edit(f"**SEARCHING...!\n `{query}`**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        # Sanitize the filename by removing invalid characters
        thumb_name = re.sub(r'[<>:"/\\|?*]', '', thumb_name)
        with open(thumb_name, 'wb') as f:
            f.write(thumb.content)
        performer = f"[Kᴇsʜᴀᴠ]"
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    except Exception as e:
        return await m.edit("**Fᴏᴜɴᴅ Nᴏᴛʜɪɴɢ Pʟᴇᴀsᴇ Cᴏʀʀᴇᴄᴛ Tʜᴇ Sᴘᴇʟʟɪɴɢ Oʀ Cʜᴇᴄᴋ Tʜᴇ LIɴᴋ**")

    await m.edit("**DOWNLOADING...!**")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        cap = "\n**BY › [⌯ Kᴇsʜᴀᴠ࿐ 🕊](https://t.me/FORBIDDEN_XD)**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await update.message.reply_audio(
            audio_file,
            caption=cap,
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name,
            reply_to_message_id=update.message.reply_to_message.id
        )
        await m.delete()
    except Exception as e:
        await m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        # print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

  ######
