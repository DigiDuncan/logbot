import asyncio
from importlib import resources as pkg_resources

from discord import Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from logbot import data

bot = commands.Bot(intents=Intents.default(), command_prefix = 'dontusethis')
slash = SlashCommand(bot)

TOKEN = pkg_resources.read_text(data, "_AUTHTOKEN")


@slash.slash(name="test")
async def test(ctx: SlashContext):
    embed = Embed(title="Embed Test")
    await ctx.send(embed=embed)


def main():
    # Remove the default help command
    bot.remove_command("help")

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    def on_disconnect():
        print("Disconnected! :sob:")

    bot.run(TOKEN)
    on_disconnect()


if __name__ == "__main__":
    main()
