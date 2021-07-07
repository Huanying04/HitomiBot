import io
import random

import discord
import pixiv
from artworks import illustration
from discord import File
from pixiv_keywords import PixivSearchOrder, PixivSearchArtworkType, PixivSearchSMode, PixivSearchType, PixivSearchMode, \
    PixivIllustrationSize

from command import Command
from config import config


class RandomPixivImgCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = 'randomAnimeImage'
        self.aliases = ["anime", "illustration", "randomAnime", "ra", "ri", "a", "i"]

    async def run(self, ctx, *args):
        keywords = config.read_config()['rand_p_srch_kywrd']
        keyword = random.choice(keywords)

        order = PixivSearchOrder.NEW_TO_OLD
        temp_s_result = pixiv.search(keyword, 1, PixivSearchArtworkType.ILLUSTRATIONS, order, PixivSearchMode.SAFE,
                                     PixivSearchSMode.SIMILAR, PixivSearchType.ILLUST)
        last_index = temp_s_result.get_last_page_index()

        page_for_srch = random.choice(range(1, last_index))

        result = pixiv.search(keyword, page_for_srch, PixivSearchArtworkType.ILLUSTRATIONS, order, PixivSearchMode.SAFE,
                              PixivSearchSMode.SIMILAR, PixivSearchType.ILLUST)
        artwork_index = random.choice(range(0, 60))
        artwork_id = result.get_ids()[artwork_index]
        info = illustration.get_artwork_info(artwork_id)
        artwork_page = random.choice(range(0, info.get_page_count()))
        image = info.get_image(PixivIllustrationSize.REGULAR, artwork_page)
        artwork_type = info.get_image_format(PixivIllustrationSize.REGULAR, page=artwork_page)

        file = io.BytesIO(image)
        filename = f'{info.get_id()}_p{artwork_page}.{artwork_type}'
        attachment = File(file, filename=filename)

        embed = discord.Embed()
        embed.title = "隨機pixiv插畫"
        embed.add_field(name="ID", value=f'[{info.get_id()}](https://www.pixiv.net/artworks/{info.get_id()})',
                        inline=True)
        embed.add_field(name="頁碼", value=str(artwork_page), inline=True)
        embed.set_image(url="attachment://" + filename)

        await ctx.send(file=attachment, embed=embed)
