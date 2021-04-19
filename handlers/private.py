from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAADBQAD9QIAAs-44VagBw6cz8jUvAI")
    await message.reply_text(
        f"""**Halo, saya adalah {bn}🎵

Saya adalah bot Music yang dirancang khusus untuk menemani anda memutar musik dalam grup melalui obrolan suara.
Berikut dibawah ini adalah kontak owner bot dan cara penggunaanya.

Tambahkan saya ke grup Anda dan mainkan musik dengan bebas!**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🛠 Cara Penggunaan 🛠", url="https://t.me/tutorilmrmusik/3")
                  ],[
                    InlineKeyboardButton(
                        "💀 Instagram", url="https://Instagram.com/xrrmli"
                    ),
                    InlineKeyboardButton(
                        "💀 Owner", url="https://t.me/mentalbrikden"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "➕ Tambahkan ke Grup Anda ➕", url="https://t.me/ilmrmusikbot?startgroup=true"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**Group Music Player Online ✅**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔊 Channel", url="https://t.me/tutorilmrmusik")
                ]
            ]
        )
   )


