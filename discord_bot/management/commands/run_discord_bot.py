import asyncio
import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from asgiref.sync import sync_to_async

from discord_bot.services.qa_service.qa_pipeline import run_qa_pipeline

import discord

logger = logging.getLogger(__name__)

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user}!")


@client.event
async def on_message(message):
    if message.author == client.user:
        # Ignore messages from the bot itself
        return

    if (
        message.guild.id not in settings.DISCORD_ALLOWED_GUILD_IDS
        or message.channel.id not in settings.DISCORD_ALLOWED_CHANNEL_IDS
    ):
        # Ignore messages from other guilds or channels
        logger.debug(f"Ignoring message from {message.guild}/{message.channel}")
        return

    logger.info(
        dict(
            server=str(message.guild),
            channel=str(message.channel),
            message=str(message.content),
        )
    )

    thread = await message.create_thread(name="Bot Answer Thread")

    async with thread.typing():
        try:
            await thread.edit(archived=True)

            result = await sync_to_async(run_qa_pipeline)(message.content)

            answer = result["answer"]
            source_urls = result["source_urls"]

            if len(source_urls) == 0:
                answer_embed = discord.Embed(
                    description="Unable to answer the query in the given context.",
                    color=0x00FF00,
                )
                embeds = [answer_embed]
            else:
                answer_embed = discord.Embed(
                    description=answer,
                    color=0x00FF00,
                )
                source_embed = discord.Embed(
                    description="Sources:\n"
                    + "\n".join([f"- {url}" for url in source_urls]),
                    color=0x00FF00,
                )
                embeds = [answer_embed, source_embed]

            thread_message = await thread.send(embeds=embeds, silent=True)

            await thread_message.add_reaction("👍")
            await thread_message.add_reaction("👎")

            await thread.edit(archived=True)
        except Exception as e:
            logger.exception(e)


class Command(BaseCommand):
    help = "Runs the Discord bot."

    def handle(self, *args, **options):
        logger.info("Starting Discord bot")

        client.run(settings.DISCORD_BOT_TOKEN)
