import io
import logging
from importlib import resources as pkg_resources

from discord import File, Intents
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from digiformatter import logger as digilogger

from logbot import data
from logbot.lib.enums import ApplicationCommandOptionType, LogLevel


bot = commands.Bot(intents=Intents.default(), command_prefix = 'dontusethis')
slash = SlashCommand(bot, sync_commands=True)

TOKEN = pkg_resources.read_text(data, "_AUTHTOKEN")

guild_ids = [870333158577569833, 913276284455485481]

logging.basicConfig(level = LogLevel.CMD)
dfhandler = digilogger.DigiFormatterHandler()
dfhandler.setLevel(LogLevel.CMD)

logger = logging.getLogger("logbot")
logger.setLevel(LogLevel.CMD)
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)


@slash.slash(name = "log",
             description = "Log an amount of messages from a channel.",
             options = [
                 {
                    "name": "amount",
                    "type": ApplicationCommandOptionType.INTEGER,
                    "description": "The amount of messages to log.",
                    "required": False
                 }
             ],
             guild_ids = guild_ids)
async def _log(ctx: SlashContext, amount: int = None):
    logger.log(LogLevel.CMD, f"{ctx.author.name}: {ctx.guild.name} | {ctx.channel.name}")
    logger.log(LogLevel.CMD, f"/log {amount if amount is not None else 'all'}")

    if amount is not None and amount < 1:
        logger.warn("Amount must be greater than 0.")
        await ctx.send("You must log at least 1 message.")
        return

    # Get requested amount of messages
    await ctx.defer()
    messages = await ctx.channel.history(limit = amount).flatten()
    logger.info(f"Logged {len(messages)} messages.")
    await ctx.send(f"{len(messages)} messages logged. Generating file...")

    # Array of lines to write to file
    lines = []

    # Reverse the messages (they come in newest first)
    messages = messages[::-1]

    # Don't say the same name over and over, and format names nicely
    last_name = None
    indent_size = max(len(message.author.name) for message in messages) + 2
    indent = " " * indent_size

    # Write each message to the file
    for message in messages:
        # Add the name if it's new
        if message.author.name != last_name:
            last_name = message.author.name
            name = (message.author.name + ':')
            lines.append(f"{name}\n")

        if message.content != "":
            for line in message.content.splitlines():
                lines.append(f"{indent}{line}\n")

        # Add attachment URLs
        if message.attachments:
            for attachment in message.attachments:
                lines.append(f"{indent}{attachment.url}\n")

    # Write the file
    file = io.StringIO(''.join(lines))
    logger.info("File generated.")

    # Send the file to the channel
    filename = f"{ctx.channel.name}-{ctx.message.created_at.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    await ctx.send("File generated!", file = File(fp = file, filename = filename))
    logger.info("File sent.")


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
