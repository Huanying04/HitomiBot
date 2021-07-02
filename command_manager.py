import sys

from command import Command
from config import config

commands = []


def register(cmd: Command):
    commands.append(cmd)


async def handle(event, message: str):
    for command in commands:
        split_msg = message.split(' ')

        if split_msg[0].startswith(config.read_config()['prefix']):
            message_cmd_name = split_msg[0][2:]
            if message_cmd_name == command.name or message_cmd_name in command.aliases:
                split_msg.pop(0)
                print(split_msg)
                try:
                    await command.run(event, split_msg)
                except:
                    e = sys.exc_info()[0]
                    await event.channel.send('錯誤發生: ' + e.__name__)
