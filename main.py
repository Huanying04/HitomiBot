from discord.ext import commands

import command_manager
from commands.direct_pixiv_img import DirectPixivImgCommand
from commands.random_pixiv_img import RandomPixivImgCommand
from config import config
import pyxiv


if __name__ == '__main__':
    token = config.read_config()['token']
    prefix = config.read_config()['prefix']

    client = commands.Bot(command_prefix=prefix, case_insensitive=True)

    pyxiv.set_php_sessid(config.read_config()['pixiv_phpsessid'])
    pyxiv.set_user_agent(config.read_config()['user_agent'])

    all_cmd = [DirectPixivImgCommand(), RandomPixivImgCommand()]
    all_cmd_name = list()

    for cmd in all_cmd:
        command_manager.register(cmd)
        all_cmd_name.append(cmd.name)
        all_cmd_name = all_cmd_name + cmd.aliases

    @client.event
    async def on_ready():
        print(f'{client.user} is ready.')

    @client.command(name='', aliases=all_cmd_name)
    async def run_command(ctx, *args):
        msg = ctx.message.content
        cmd_name = msg.split(" ", 1)[0][len(prefix):]
        await command_manager.handle(ctx, cmd_name, *args)

    client.run(token)
