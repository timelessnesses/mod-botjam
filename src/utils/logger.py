import typing
from enum import Enum

import aiofiles
import discord
import plum

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


@plum.dispatch
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
                "type": type.value,
                "actioner": actioner.id,
                "target": target.id,
                "when": when,
                "reason": reason,
                "duration": duration,
            }
        )
    except KeyError:
        data[str(guild)] = {
            "logging": [
                {
                    "id": id,
                    "type": type.value,
                    "actioner": actioner.id,
                    "target": target.id,
                    "when": when,
                    "reason": reason,
                }
            ]
        }
    async with aiofiles.open("db/logging.json", "w") as fp:
        await json.dump(data, fp)


@plum.dispatch
async def log(
    id: str,
    guild: int,
    type: Types,
    actioner: typing.Union[discord.Member, discord.User],
    target: typing.Union[discord.Member, discord.User],
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
                "type": type.value,
                "actioner": actioner.id,
                "target": target.id,
                "when": when,
                "reason": reason,
                "duration": duration,
            }
        )
    except KeyError:
        data[str(guild)] = {
            "logging": [
                {
                    "id": id,
                    "type": type.value,
                    "actioner": actioner.id,
                    "target": target.id,
                    "when": when,
                    "reason": reason,
                }
            ]
        }
    async with aiofiles.open("db/logging.json", "w") as fp:
        await json.dump(data, fp)
