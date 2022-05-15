from PhixyBot.events import register
from PhixyBot import OWNER_ID,SUDO_USERS
from PhixyBot import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont
import shutil 
import random, re
import glob
import time
from telethon.tl.types import InputMessagesFilterPhotos


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"





@register(pattern="^/ylogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo..')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./PhixyBot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./PhixyBot/resources/Streamster.ttf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "PhixyLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Powered by @TeamPhixY ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')



@register(pattern="^/rlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo..')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./PhixyBot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "red"
    shadowcolor = "blue"
    font = ImageFont.truetype("./PhixyBot/resources/Streamster.ttf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="red")
    fname2 = "PhixyLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Powered by @TeamPhixY ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')



@register(pattern="^/wwlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo..')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./PhixyBot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./PhixyBot/resources/Streetwear.ttf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="white")
    fname2 = "PhixyLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Powered by @TeamPhixY ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')


@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo..')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./PhixyBot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Phixy/resources/1.ttf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "PhixyLogo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Powered by @TeamPhixY ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')

@register(pattern="^/biglogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo... wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Phixy/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Phixy/resources/Chopsic.otf", 950)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "Phixy.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Powered by @TeamPhixY ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')

   
@register(pattern="^/wlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo... wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./Phixy/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./Phixy/resources/Maghrib.ttf", 1000)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white")
    fname2 = "Phixy.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @SophiaSLBot ")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Go to Help From  @TeamPhixY, {e}')




file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
*Commands :*
〄 /logo text :  Create your logo with your name
〄 /wwlogo text :  Create your logo with your name
〄 /rlogo text :  Create your logo with your name
〄 /ylogo text :  Create your logo with your name
〄 /biglogo text :  Create your logo Bigger Than `logo`
〄 /wlogo text :  Create your logo with your name

*Powered by* @TeamPhixY ❤️
 """
__mod_name__ = "Lᴏɢᴏ Mᴀᴋᴇʀ"
