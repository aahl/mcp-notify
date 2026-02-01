import os
import io
import re
import base64
import telegramify_markdown
from telegram import Bot, InputFile
from fastmcp import FastMCP
from pydantic import Field

TELEGRAM_DEFAULT_CHAT = os.getenv("TELEGRAM_DEFAULT_CHAT", "0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BASE_URL = os.getenv("TELEGRAM_BASE_URL") or "https://api.telegram.org"
TELEGRAM_MARKDOWN_V2 = "MarkdownV2"


md_customize = telegramify_markdown.customize.get_runtime_config()
md_customize.markdown_symbol.head_level_1 = "1️⃣"
md_customize.markdown_symbol.head_level_2 = "2️⃣"
md_customize.markdown_symbol.head_level_3 = "3️⃣"
md_customize.markdown_symbol.head_level_4 = "4️⃣"


def add_tools(mcp: FastMCP, logger=None):
    bot = Bot(
        TELEGRAM_BOT_TOKEN,
        base_url=f"{TELEGRAM_BASE_URL}/bot",
        base_file_url=f"{TELEGRAM_BASE_URL}/file/bot",
    ) if TELEGRAM_BOT_TOKEN else None


    @mcp.tool(
        title="Telegram send text",
        description="Send text or markdown message via telegram bot",
    )
    async def tg_send_message(
        text: str = Field(description="Text of the message to be sent, 1-4096 characters after entities parsing"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the message text. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if not bot:
            return "Please set the `TELEGRAM_BOT_TOKEN` environment variable"
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            text = telegramify_markdown.markdownify(text)
        res = await bot.send_message(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            text=text,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
            reply_to_message_id=reply_to_message_id or None,
        )
        return res.to_json()


    @mcp.tool(
        title="Telegram send photo",
        description="Send photo via telegram bot",
    )
    async def tg_send_photo(
        photo: str = Field(description="Photo URL or base64 data URI (e.g., data:image/png;base64,..."),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Photo caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)

        if photo.startswith("data:"):
            match = re.match(r"data:image/([^;]+);base64,(.*)", photo)
            if not match:
                return {"error": "Invalid base64 data URL format"}
            try:
                datas = base64.b64decode(match.group(2))
                photo = InputFile(io.BytesIO(datas), f"image.{match.group(1)}")
            except Exception as e:
                return {"error": f"Failed to decode base64: {str(e)}"}

        res = await bot.send_photo(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            photo=photo,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
            reply_to_message_id=reply_to_message_id or None,
        )
        return res.to_json()


    @mcp.tool(
        title="Telegram send video",
        description="Send video via telegram bot",
    )
    async def tg_send_video(
        video: str = Field(description="Video URL or base64 data URI (e.g., data:video/mp4;base64,..."),
        cover: str = Field("", description="Cover for the video in the message. Optional"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Video caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)

        if video.startswith("data:"):
            match = re.match(r"data:video/([^;]+);base64,(.*)", video)
            if not match:
                return {"error": "Invalid base64 data URL format"}
            try:
                datas = base64.b64decode(match.group(2))
                video = InputFile(io.BytesIO(datas), f"video.{match.group(1)}")
            except Exception as e:
                return {"error": f"Failed to decode base64: {str(e)}"}

        res = await bot.send_video(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            video=video,
            cover=cover or None,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
            reply_to_message_id=reply_to_message_id or None,
        )
        return res.to_json()


    @mcp.tool(
        title="Telegram send audio",
        description="Send audio via telegram bot",
    )
    async def tg_send_audio(
        audio: str = Field(description="Audio URL or base64 data URI (e.g., data:audio/wav;base64,..."),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Audio caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)

        if audio.startswith("data:"):
            match = re.match(r"data:audio/([^;]+);base64,(.*)", audio)
            if not match:
                return {"error": "Invalid base64 data URL format"}
            try:
                datas = base64.b64decode(match.group(2))
                audio = InputFile(io.BytesIO(datas), f"audio.{match.group(1)}")
            except Exception as e:
                return {"error": f"Failed to decode base64: {str(e)}"}

        res = await bot.send_audio(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            audio=audio,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
            reply_to_message_id=reply_to_message_id or None,
        )
        return res.to_json()


    @mcp.tool(
        title="Telegram send file",
        description="Send general files via telegram bot",
    )
    async def tg_send_file(
        url: str = Field(description="File URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="File caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)
        res = await bot.send_document(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            document=url,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
            reply_to_message_id=reply_to_message_id or None,
        )
        return res.to_json()
