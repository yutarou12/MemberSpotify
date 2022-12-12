import logging
import traceback
import os
import requests

import discord
from discord.ext import commands
from discord import app_commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='now')
    async def now_cmd(self, interaction):
        """
        現在聴いている曲を表示します。
        """

        member = interaction.guild.get_member(interaction.user.id)
        if not member:
            return await interaction.response.send_message('メンバーを取得できませんでした。', ephemeral=True)

        if member.activities:
            return await interaction.response.send_message('Spotifyで再生していないようです。', ephemeral=True)

        m_activity = None
        for act in member.activities:
            if isinstance(act, discord.Spotify):
                m_activity = act
                break
        if m_activity:
            text = f'Now Listening Music 🎶 - `{member.name}`\n' \
                   f'Music Title: `{m_activity.title}({m_activity.artist})`\n' \
                   f'{m_activity.track_url}'
            await interaction.response.send_message(text, ephemeral=False)
        else:
            await interaction.response.send_message('Spotifyで再生していないようです。', ephemeral=True)



async def setup(bot):
    await bot.add_cog(Core(bot))
