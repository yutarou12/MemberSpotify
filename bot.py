import os
import logging

import discord
from discord import Interaction
from discord.app_commands import AppCommandError
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

config = {
    'prefix': os.getenv('PREFIX'),
    'token': os.getenv('DISCORD_BOT_TOKEN'),
    'oauth_url': discord.utils.oauth_url(os.getenv('BOT_ID'),
                                         permissions=discord.Permissions(277025778752),
                                         scopes=['bot', 'applications.commands'])
}

extensions_list = ['jishaku', 'Core', 'Main']


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError):
        tracebacks = getattr(error, 'traceback', error)
        tracebacks = ''.join(traceback.TracebackException.from_exception(tracebacks).format())
        logging.error(tracebacks)

    async def get_context(self, message, *args, **kwargs):
        return await super().get_context(message, *args, **kwargs)

    async def setup_hook(self):
        for extension in extensions_list:
            self.bot.load_extension(f'cogs.{extension}')


intents = discord.Intents.all()
intents.typing = False
intents.dm_typing = False

bot = MyBot(
    command_prefix=commands.when_mentioned_or(config['prefix']),
    intents=intents,
    help_command=None,
    allowed_mentions=discord.AllowedMentions(replied_user=False, everyone=False),
)


@bot.event
async def on_ready():
    print(f'{bot.user.name} でログインしました')
    print(f'サーバー数: {len(bot.guilds)}')
    await bot.change_presence(
        activity=discord.Game(name=f'/help | Get a MemberActivity')
    )
    await bot.tree.sync()


if __name__ == '__main__':
    bot.config = config

    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
