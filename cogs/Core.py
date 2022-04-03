import os
import requests
import codecs
import base64

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

        member = ctx.guild.get_member(ctx.author.id)
        if member and member.activities:
            m_activity = None
            for act in member.activities:
                if isinstance(act, discord.Spotify):
                    m_activity = act
                    break
            if m_activity:
                client_id = os.environ.get('SPOTIFY_CLIENT_ID')
                client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
                client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

                spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                result = spotify.track(m_activity.track_id)
                release_date = result['album']['release_date'].replace('-', '/', 2) if result else '取得不可'

                embed = discord.Embed(title=f'{member.name} が聴いている曲')
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(name='曲名', value=m_activity.title)
                embed.add_field(name='アーティスト', value=m_activity.artist)
                embed.add_field(name='アルバム', value=m_activity.album, inline=False)
                embed.add_field(name='曲の長さ', value=str(m_activity.duration).split('.')[0])
                embed.add_field(name='リリース日', value=release_date)
                embed.add_field(name='URL', value=f'[自分も聴く]({m_activity.track_url})', inline=False)
                embed.set_image(url=m_activity.album_cover_url)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond('現在、Spotifyで再生していないようです。', ephemeral=True)


"""
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.channel_id == 928907253782806568:
            return

        if str(payload.emoji) == '✅':
            channel = self.bot.get_channel(payload.channel_id)
            if channel:
                member = channel.guild.get_member(payload.user_id)
                if member.activities:
                    m_activity = None
                    for act in member.activities:
                        if isinstance(act, discord.Spotify):
                            m_activity = act
                            break
                    if m_activity:
                        headers = {
                            "Accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {os.environ.get('SPOTIFY_API')}"
                        }
                        r = requests.get(f'https://api.spotify.com/v1/tracks/{m_activity.track_id}', headers=headers)
                        release_date = r.json()['album']['release_date'] if r.status_code == 200 else '取得不可'

                        embed = discord.Embed(title=f'{member.name} が聴いている曲')
                        embed.set_thumbnail(url=member.display_avatar.url)
                        embed.add_field(name='曲名', value=m_activity.title)
                        embed.add_field(name='アーティスト', value=m_activity.artist)
                        embed.add_field(name='アルバム', value=m_activity.album, inline=False)
                        embed.add_field(name='曲の長さ', value=str(m_activity.duration).split('.')[0])
                        embed.add_field(name='リリース日', value=release_date.replace('-', '/', 2))
                        embed.add_field(name='URL', value=f'[自分も聴く]({m_activity.track_url})', inline=False)
                        embed.set_image(url=m_activity.album_cover_url)
                        await channel.send(embed=embed)
"""


def setup(bot):
    bot.add_cog(Core(bot))
