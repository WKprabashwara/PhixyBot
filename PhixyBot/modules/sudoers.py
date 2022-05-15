"""
XIT License 2021

Copyright (c) 2021 WKRPrabashwara


"""
import asyncio
import os
import subprocess
import time

import psutil
from pyrogram import filters

from PhixyBot import (bot_start_time, DEV_USERS, pbot)
from PhixyBot.utils import formatter




# Stats Module

async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
rᴏᴏᴛ :@PhixYBot ~ $ bᴀꜱʜ
------------------
🕔 Uptime: {formatter.get_readable_time((bot_uptime))}
👁‍🗨 Bot: {round(process.memory_info()[0] / 1024 ** 2)} MB
⏳ Cpu: {cpu}%
📟 Ram: {mem}%
💾 Disk: {disk}%

------------------
"""
    return stats


