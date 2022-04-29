#
# Copyright (C) 2021-2022 by devilxdereor@Github, < https://github.com/devilxdereor >.
#
# This file is part of < https://github.com/devilxdereor/DEVILXMUSIC > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/devilxdereor/DEVILXMUSIC/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from DEVILXMUSIC import LOGGER, app, userbot
from DEVILXMUSIC.core.call import Yukki
from DEVILXMUSIC.plugins import ALL_MODULES
from DEVILXMUSIC.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("DEVILXMUSIC").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("DEVILXMUSIC").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("DEVILXMUSIC.plugins" + all_module)
    LOGGER("DEVILXMUSIC.plugins").info(
        "Successfully Imported Modules "
    )
    await userbot.start()
    await Yukki.start()
    try:
        await Yukki.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("DEVILXMUSIC").error(
            "[ERROR] - \n\nPlease turn on your Logger Group's Voice Call. Make sure you never close/end voice call in your log group"
        )
        sys.exit()
    except:
        pass
    await DEVILXMUSIC.decorators()
    LOGGER("DEVILXMUSIC").info("DEVILXMUSIC  Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("DEVILXMUSIC").info("Stopping DEVILXMUSIC Bot! GoodBye")
