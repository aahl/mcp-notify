import os
import logging
import telegramify_markdown
from telegram import Bot
from fastmcp import FastMCP
from pydantic import Field

_LOGGER = logging.getLogger(__name__)

TELEGRAM_DEFAULT_CHAT = os.getenv("TELEGRAM_DEFAULT_CHAT", "0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BASE_URL = os.getenv("TELEGRAM_BASE_URL") or "https://api.telegram.org"
TELEGRAM_MARKDOWN_V2 = "MarkdownV2"
TELEGRAM_MARKDOWN_RULE = """
Pass `MarkdownV2` in the `parse_mode` field. Please strictly follow the following rules:
- Any character with code between 1 and 126 inclusively can be escaped anywhere with a preceding backslash, in which case it is treated as an ordinary character and not a part of the markup. This implies that backslash usually must be escaped with a preceding backslash.
- Inside pre and code entities, all '`' and backslash must be escaped with a preceding backslash.
- Inside the (...) part of the inline link and custom emoji definition, all ')' and backslash must be escaped with a preceding backslash.
- In all other places characters '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' MUST be escaped with the preceding backslash. **Extremely important !!!**
- In case of ambiguity between italic and underline entities __ is always greedily treated from left to right as beginning or end of an underline entity, so instead of ___italic underline___ use ___italic underline_**__, adding an empty bold entity as a separator.
- Don't support for multi-level heads, all '#' must be escaped with a preceding backslash to indicate tags.
- Code blocks are enclosed with three backticks.
Only supports the following syntax in your message:
```MarkdownV2
*bold \\*text*
_italic \\*text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://example\\.com)
[inline mention of a user](tg://user?id=123)
![👍](tg://emoji?id=123456)
`inline fixed-width code`
>Block quotation started
>Block quotation continued
>The last line of the block quotation
**>The expandable block quotation started right after the previous block quotation
>It is separated from the previous block quotation by an empty bold entity
>Expandable block quotation continued
>Hidden by default part of the expandable block quotation started
>Expandable block quotation continued
>The last line of the expandable block quotation with the expandability mark||
```
"""


md_customize = telegramify_markdown.customize.get_runtime_config()
md_customize.markdown_symbol.head_level_1 = "1️⃣"
md_customize.markdown_symbol.head_level_2 = "2️⃣"
md_customize.markdown_symbol.head_level_3 = "3️⃣"
md_customize.markdown_symbol.head_level_4 = "4️⃣"


def add_tools(mcp: FastMCP):
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
        photo: str = Field(description="Photo URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Photo caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)
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
        video: str = Field(description="Video URL"),
        cover: str = Field("", description="Cover for the video in the message. Optional"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Video caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)
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
        audio: str = Field(description="Audio URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Audio caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
        reply_to_message_id: int = Field(0, description="Identifier of the message that will be replied to"),
    ):
        if parse_mode == TELEGRAM_MARKDOWN_V2:
            caption = telegramify_markdown.markdownify(caption)
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


    @mcp.tool(
        title="Telegram markdown rule",
        description="Telegram supports Markdown formatting. Must use this tool before sending markdown to Telegram.",
    )
    def tg_markdown_rule():
        return TELEGRAM_MARKDOWN_RULE
