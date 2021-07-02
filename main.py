import io
import random
import traceback

import discord
from artworks import illustration
from discord import File
from discord.ext import commands
from pixiv_keywords import PixivIllustrationSize, PixivSearchOrder, PixivSearchArtworkType, PixivSearchSMode, \
    PixivSearchType, PixivSearchMode

from config import config
import pyxiv
import pixiv

if __name__ == '__main__':
    token = config.read_config()['token']
    prefix = config.read_config()['prefix']

    client = commands.Bot(command_prefix=prefix, case_insensitive=True)

    pyxiv.set_php_sessid(config.read_config()['pixiv_phpsessid'])
    pyxiv.set_user_agent(config.read_config()['user_agent'])


    @client.event
    async def on_ready():
        print(f'{client.user} is ready.')


    @client.command(name="pixiv")
    async def direct_pixiv_image(ctx, *args):
        async with ctx.typing():
            try:
                info = illustration.get_artwork_info(args[0])

                page = (0 if args[1] > info.get_page_count() else args[1]) if len(args) > 1 else 0

                image = info.get_image(PixivIllustrationSize.REGULAR, page)
                file = io.BytesIO(image)
                filename = f'{args[0]}_p{page}.{info.get_image_format(PixivIllustrationSize.REGULAR)}'
                attachment = File(file, filename=filename)

                embed = discord.Embed()
                embed.add_field(name="標題", value=info.get_title(), inline=False)
                embed.add_field(name="簡介", value=info.get_description(), inline=False)
                # embed.add_field(name="標籤", value=info.get_tags(), inline=False)
                embed.add_field(name="作者", value=info.get_author_name(), inline=False)
                embed.add_field(name="ID", value=f'[{info.get_id()}](https://www.pixiv.net/artworks/{info.get_id()})',
                                inline=True)
                embed.add_field(name="頁碼", value=page, inline=False)
                embed.add_field(name="頁數", value=info.get_page_count(), inline=True)
                embed.set_image(url="attachment://" + filename)

                await ctx.send(file=attachment, embed=embed)
            except Exception as e:
                await ctx.send("發生錯誤！" + str(e.__class__) + str(e.args))
                traceback.print_exc()


    @client.command(aliases=["anime", "illustration", "randomAnime", "ra", "ri", "a", "i"])
    async def random_anime_illustration(ctx):
        async with ctx.typing():
            try:
                keywords = config.read_config()['rand_p_srch_kywrd']
                keyword = random.choice(keywords)

                order = PixivSearchOrder.NEW_TO_OLD
                temp_s_result = pixiv.search(keyword, 1, PixivSearchArtworkType.ILLUSTRATIONS, order, PixivSearchMode.SAFE,
                                             PixivSearchSMode.SIMILAR, PixivSearchType.ILLUST)
                last_index = temp_s_result.get_last_page_index()

                page_for_srch = random.choice(range(1, last_index))

                result = pixiv.search(keyword, page_for_srch, PixivSearchArtworkType.ILLUSTRATIONS, order, PixivSearchMode.SAFE,
                                      PixivSearchSMode.SIMILAR, PixivSearchType.ILLUST)
                artwork_index = random.choice(range(0, 60 + 1))
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
                                inline=False)
                embed.add_field(name="ID", value=f'[{info.get_id()}](https://www.pixiv.net/artworks/{info.get_id()})',
                                inline=True)
                embed.set_image(url="attachment://" + filename)

                await ctx.send(file=attachment, embed=embed)
            except Exception as e:
                await ctx.send("發生錯誤！" + str(e.__class__) + str(e.args))
                traceback.print_exc()


    client.run(token)
