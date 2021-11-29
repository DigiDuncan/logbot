from digiformatter import logger as digilogger


class ApplicationCommandOptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    FLOAT = 10


class LogLevel:
    LOGIN = digilogger.addLogLevel("login", fg="cyan")
    CMD = digilogger.addLogLevel("cmd", fg="grey_50", base="DEBUG", prefix="CMD")
