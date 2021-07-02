import traceback

from command import Command

commands = []


def register(cmd: Command):
    commands.append(cmd)


async def handle(ctx, name, *args):
    for command in commands:
        if name == command.name or name in command.aliases:
            async with ctx.typing():
                try:
                    await command.run(ctx, *args)
                except Exception as e:
                    await ctx.send("發生錯誤！" + str(e.__class__) + str(e.args))
                    traceback.print_exc()
