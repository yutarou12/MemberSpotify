import discord
from discord import app_commands
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='about')
    async def about(self, interaction):
        """
        このBOTについての説明を表示します。
        """
        embed = discord.Embed(title=f'{self.bot.user.name} について',
                              description='> このBotは、メンバーが Spotify で聞いている曲を取得して、\n'
                                          '> その曲をチャンネルに投稿しサーバーの他メンバーと共有しやすくするために作られたBOTです。')
        embed.add_field(name='バグがあった場合', value='バグや不具合があった場合には、お手数をおかけしますが以下のサーバーへ報告お願いします。'
                                               '\n https://discord.gg/k5Feum44gE ', inline=False)
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='help')
    async def help_cmd(self, interaction):
        """
        このBOTのヘルプを表示します。
        """

        embed = discord.Embed(title='ヘルプ')
        embed.add_field(name='help', value='このコマンドのヘルプ', inline=False)
        embed.add_field(name='about', value='このBotについて', inline=False)
        """ embed.add_field(name='setting', value='共有するチャンネルの設定', inline=False) """
        embed.add_field(name='now', value='聞いている曲の情報を取得', inline=False)

        return await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Main(bot))
