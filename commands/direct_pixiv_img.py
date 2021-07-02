import io

import discord
from artworks import illustration
from discord import File
from pixiv_keywords import PixivIllustrationSize

from command import Command


class DirectPixivImgCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = 'pixiv'

    async def run(self, ctx, *args):
        info = illustration.get_artwork_info(args[0])

        page = (0 if args[1] > info.get_page_count() else args[1]) if len(args) > 1 else 0

        image = info.get_image(PixivIllustrationSize.REGULAR, page)
        file = io.BytesIO(image)
        filename = f'{args[0]}_p{page}.{info.get_image_format(PixivIllustrationSize.REGULAR)}'
        attachment = File(file, filename=filename)

        embed = discord.Embed()
        embed.add_field(name="標題", value=info.get_title(), inline=False)
        embed.add_field(name="簡介", value='\u200B' if info.get_description()=='' else info.get_description(),
                        inline=False)
        # embed.add_field(name="標籤", value=info.get_tags(), inline=False)
        embed.add_field(name="作者", value=info.get_author_name(), inline=False)
        embed.add_field(name="ID", value=f'[{info.get_id()}](https://www.pixiv.net/artworks/{info.get_id()})',
                        inline=True)
        embed.add_field(name="頁碼", value=page, inline=False)
        embed.add_field(name="頁數", value=info.get_page_count(), inline=True)
        embed.set_image(url="attachment://" + filename)

        await ctx.send(file=attachment, embed=embed)
