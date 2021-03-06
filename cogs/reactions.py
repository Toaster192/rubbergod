import discord
from discord.ext import commands

import utils
from config.app_config import Config


class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Catch reaction, get all properties and then call proper cog/s"""
        ctx = await utils.reaction_get_ctx(self.bot, payload)
        if ctx is None:
            return

        cogs = []

        if (
            ctx["message"].embeds
            and ctx["message"].embeds[0].title is not discord.Embed.Empty
            and "reviews" in ctx["message"].embeds[0].title
        ):
            cogs.append(self.bot.get_cog("Review"))
        if ctx["emoji"] == "📌":
            cogs.append(self.bot.get_cog("AutoPin"))
        if ctx["message"].embeds and ctx["message"].embeds[0].title == "Rubbergod":
            cogs.append(self.bot.get_cog("Base"))
        if ctx["channel"].id not in Config.role_channels:
            cogs.append(self.bot.get_cog("Karma"))
        else:
            cogs.append(self.bot.get_cog("ReactToRole"))
        if (
            ctx["emoji"] == "❎"
            and payload.channel_id in Config.deduplication_channels
            and not payload.member.bot
            and ctx["message"].author.bot
        ):
            cogs.append(self.bot.get_cog("Warden"))

        for cog in cogs:
            # check if cog is loaded
            if cog:
                await cog.hadle_reaction(ctx)


def setup(bot):
    bot.add_cog(Reaction(bot))
