# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Environment variables for API credentials
API_ID = os.environ.get("API_ID", "24473318")
API_HASH = os.environ.get("API_HASH", "e7dd0576c5ac0ff8f90971d6bb04c8f5")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Define the owner's user ID
OWNER_ID = 5840594311   # Replace with the actual owner's user ID

# Lists to store authorized users,channels,and groups
authorized_users = []
authorized_channels = []
authorized_groups = []

# Function to check if a user is authorized
def is_authorized(user_id):
    return user_id in SUDO_USERS

# Function to check if a user is authorized
def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS

# Function to extract the title from the text file
def extract_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()  # Read the first line and remove extra spaces
        return first_line if first_line else "Untitled"  # Return "Untitled" if the file is empty


# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Center the text dynamically based on terminal width
centered_text = "◦•●◉✿ 𝕰𝖓𝖌𝖎𝖓𝖊𝖊𝖗𝖘 𝕭𝖆𝖇𝖚 ✿◉●•◦".center(40)

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Engineers_Babu"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/Engineers_Babu"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/Engineersbabuupdates"),
        ],
    ]
)

# Command to add a channel ID to the authorized list
def add_channel(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        channel_id = int(context.args[0])  # Get the channel ID from the command arguments
        if channel_id not in authorized_channels:
            authorized_channels.append(channel_id)
            context.message.reply_text(f"✅ Channel ID {channel_id} has been authorized.")
        else:
            context.message.reply_text(f"ℹ️ Channel ID {channel_id} is already authorized.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /add_channel <channel_id>")

# Command to remove a channel ID from the authorized list
def remove_channel(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        channel_id = int(context.args[0])  # Get the channel ID from the command arguments
        if channel_id in authorized_channels:
            authorized_channels.remove(channel_id)
            context.message.reply_text(f"✅ Channel ID {channel_id} has been removed.")
        else:
            context.message.reply_text(f"ℹ️ Channel ID {channel_id} is not in the authorized list.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /remove_channel <channel_id>")
            
# Command to add a user ID to the authorized list
def add_user(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        user_id = int(context.args[0])  # Get the user ID from the command arguments
        if user_id not in authorized_users:
            authorized_users.append(user_id)
            context.message.reply_text(f"✅ User ID {user_id} has been authorized.")
        else:
            context.message.reply_text(f"ℹ️ User ID {user_id} is already authorized.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /add_user <user_id>")

# Command to remove a user ID from the authorized list
def remove_user(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        user_id = int(context.args[0])  # Get the user ID from the command arguments
        if user_id in authorized_users:
            authorized_users.remove(user_id)
            context.message.reply_text(f"✅ User ID {user_id} has been removed.")
        else:
            context.message.reply_text(f"ℹ️ User ID {user_id} is not in the authorized list.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /remove_user <user_id>")

# Command to add a group ID to the authorized list
def add_group(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        group_id = int(context.args[0])  # Get the group ID from the command arguments
        if group_id not in authorized_groups:
            authorized_groups.append(group_id)
            context.message.reply_text(f"✅ Group ID {group_id} has been authorized.")
        else:
            context.message.reply_text(f"ℹ️ Group ID {group_id} is already authorized.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /add_group <group_id>")

# Command to remove a group ID from the authorized list
def remove_group(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        group_id = int(context.args[0])  # Get the group ID from the command arguments
        if group_id in authorized_groups:
            authorized_groups.remove(group_id)
            context.message.reply_text(f"✅ Group ID {group_id} has been removed.")
        else:
            context.message.reply_text(f"ℹ️ Group ID {group_id} is not in the authorized list.")
    except (IndexError, ValueError):
        context.message.reply_text("❌ Usage: /remove_group <group_id>")


# Command to list all authorized channels, users, and groups
def list_authorized(context: CallbackContext) -> None:
    if not is_owner(context):
        context.message.reply_text("🚫 You are not authorized to use this command.")
        return

    response = (
        f"Authorized Users: {', '.join(map(str, authorized_channels)) or 'None'}\n"
        f"Authorized Channels: {', '.join(map(str, authorized_users)) or 'None'}\n"
        f"Authorized Groups: {', '.join(map(str, authorized_groups)) or 'None'}"
    )
    context.message.reply_text(response)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_channel", add_channel))
    dispatcher.add_handler(CommandHandler("remove_channel", remove_channel))
    dispatcher.add_handler(CommandHandler("add_user", add_user))
    dispatcher.add_handler(CommandHandler("remove_user", remove_user))
    dispatcher.add_handler(CommandHandler("add_group", add_group))
    dispatcher.add_handler(CommandHandler("remove_group", remove_group))
    dispatcher.add_handler(CommandHandler("list_authorized", list_authorized))

# Upload command handler
@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 📄')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        
        # Extract the title from the file name
        file_name = os.path.basename(x)  # Get the file name from the path
        raw_text0 = os.path.splitext(file_name)[0]  # Remove the file extension to get the title
        
        os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("**∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.**")
           os.remove(x)
           return
            
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗** **{len(links)}**\n\n**𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    

    await editable.edit("**𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸**\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now send the Thumb url/nEg » https://graph.org/file/ce1723991756e48c35aa1.jpg \n Or if don't want thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {𝗻𝗮𝗺𝗲𝟭}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎**")


bot.run()
