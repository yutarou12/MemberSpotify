import logging
import traceback
import os
import requests

import discord
from discord.ext import commands
from discord.commands import slash_command

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='now')
    async def now_cmd(self, ctx):
        """
        現在聴いている曲を表示します。
        """

        try:
            member = ctx.guild.get_member(ctx.author.id)
            if member:
                if member.activities:
                    m_activity = None
                    for act in member.activities:
                        if isinstance(act, discord.Spotify):
                            m_activity = act
                            break
                    if m_activity:
                        text = f'Now Listening Music 🎶 - `{member.name}`\n' \
                               f'Music Title: `{m_activity.title}({m_activity.artist})`\n' \
                               f'{m_activity.track_url}'
                        await ctx.respond(text, ephemeral=False)
                    else:
                        await ctx.respond('Spotifyで再生していないようです。', ephemeral=True)
                else:
                    await ctx.respond('Spotifyで再生していないようです。', ephemeral=True)
            else:
                await ctx.respond('メンバーを取得できませんでした。', ephemeral=True)
        except Exception as error:
            tracebacks = getattr(error, 'traceback', error)
            tracebacks = ''.join(traceback.TracebackException.from_exception(tracebacks).format())
            logging.error(tracebacks)


def setup(bot):
    bot.add_cog(Core(bot))
