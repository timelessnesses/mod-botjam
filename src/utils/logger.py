import typing

import aiofiles
import discord

from . import json


class Types:
    kick = "kick"
    ban = "ban"
    unban = "unban"
    warn = "warn"
    mute = "mute"
    unmute = "unmute"
    delwarn = "delwarn"
    purge = "purge"
    hackban = "hackban"
    swear = "swear"


async def log(
    id: str,
    guild: int,
    type: Types,
    actioner: typing.Union[discord.Member, discord.User],
    target: typing.Union[discord.Member, discord.User],
    when: str,
    reason: str = None,
):
    async with aiofiles.open("db/logging.json") as fp:
        data = await json.load(fp)

    try:
        data[str(guild)]["logging"].append(
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
            }
        )
    except KeyError:
        data[str(guild)]["logging"] = [
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
            }
        ]
    async with aiofiles.open("db/logging.json", "w") as fp:
        await json.dump(fp, data)


async def log_mute(
    id: str,
    guild: int,
    type: Types,
    actioner: typing.Union[discord.Member, discord.User, int],
    target: typing.Union[discord.Member, discord.User, int],
    when: str,
    reason: str = None,
    duration: int = None,
):
    async with aiofiles.open("db/logging.json") as fp:
        data = await json.load(fp)

    try:
        data[str(guild)]["logging"].append(
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
                "duration": duration,
            }
        )
    except KeyError:
        data[str(guild)]["logging"] = [
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
                "duration": duration,
            }
        ]
    async with aiofiles.open("db/logging.json", "w") as fp:
        await json.dump(fp, data)


async def del_warn_log(
    id: str,
    warn_id: str,
    guild: int,
    type: Types,
    actioner: typing.Union[discord.Member, discord.User],
    target: typing.Union[discord.Member, discord.User],
    when: str,
    reason: str = None,
):
    async with aiofiles.open("db/logging.json") as fp:
        data = await json.load(fp)

    try:
        data[str(guild)]["logging"].append(
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
            }
        )
    except KeyError:
        data[str(guild)]["logging"] = [
            {
                "id": id,
                "type": type,
                "actioner": actioner,
                "target": target,
                "when": when,
                "reason": reason,
            }
        ]
    try:
        for logs in data[str(guild)]["logging"]:
            if logs["id"] == warn_id:
                data[str(guild)]["logging"].remove(logs)
    except:
        pass
    async with aiofiles.open("db/logging.json", "w") as fp:
        await json.dump(fp, data)
