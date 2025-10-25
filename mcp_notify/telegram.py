import os
import logging
from telegram import Bot
from fastmcp import FastMCP
from pydantic import Field

_LOGGER = logging.getLogger(__name__)

TELEGRAM_DEFAULT_CHAT = os.getenv("TELEGRAM_DEFAULT_CHAT", "0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BASE_URL = os.getenv("TELEGRAM_BASE_URL") or "https://api.telegram.org"
TELEGRAM_MARKDOWN_V2 = "MarkdownV2"
TELEGRAM_MARKDOWN_RULE = """
The Bot API supports basic formatting for messages.
You can use bold, italic, underlined, strikethrough, spoiler text, block quotations as well as inline links and pre-formatted code in your bots' messages.
Telegram clients will render them accordingly. You can specify text entities directly, or use markdown-style or HTML-style formatting.
Message entities can be nested, providing following restrictions are met:
- If two entities have common characters, then one of them is fully contained inside another.
- bold, italic, underline, strikethrough, and spoiler entities can contain and can be part of any other entities, except pre and code.
- blockquote and expandable_blockquote entities can't be nested.
- All other entities can't contain each other.
Pass `MarkdownV2` in the `parse_mode` field. Use the **following syntax** in your message:
```MarkdownV2
*bold \*text*
_italic \*text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
\```
pre-formatted fixed-width code block
\```
\```python
pre-formatted fixed-width code block written in the Python programming language
\```
>Block quotation started
>Block quotation continued
>Block quotation continued
>The last line of the block quotation
**>The expandable block quotation started right after the previous block quotation
>It is separated from the previous block quotation by an empty bold entity
>Expandable block quotation continued
>Hidden by default part of the expandable block quotation started
>Expandable block quotation continued
>The last line of the expandable block quotation with the expandability mark||
```
Please note:
- Any character with code between 1 and 126 inclusively can be escaped anywhere with a preceding '\' character, in which case it is treated as an ordinary character and not a part of the markup. This implies that '\' character usually must be escaped with a preceding '\' character.
- Inside pre and code entities, all '`' and '\' characters must be escaped with a preceding '\' character.
- Inside the (...) part of the inline link and custom emoji definition, all ')' and '\' must be escaped with a preceding '\' character.
- **MUST** In all other places characters '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' must be escaped with the preceding character '\'.
- In case of ambiguity between italic and underline entities __ is always greedily treated from left to right as beginning or end of an underline entity, so instead of ___italic underline___ use ___italic underline_**__, adding an empty bold entity as a separator.
"""


def add_tools(mcp: FastMCP):
    bot = Bot(
        TELEGRAM_BOT_TOKEN,
        base_url=f"{TELEGRAM_BASE_URL}/bot",
        base_file_url=f"{TELEGRAM_BASE_URL}/file/bot",
    )


    @mcp.tool(
        description="Send text message via telegram bot",
    )
    async def tg_send_message(
        text: str = Field(description="Text of the message to be sent, 1-4096 characters after entities parsing"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the message text. [text/MarkdownV2]"),
    ):
        res = await bot.send_message(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            text=text,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
        )
        return res.to_json()


    @mcp.tool(
        description="Send photos via telegram bot",
    )
    async def tg_send_photo(
        photo: str = Field(description="Photo URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Photo caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
    ):
        res = await bot.send_photo(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            photo=photo,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
        )
        return res.to_json()


    @mcp.tool(
        description="Send video via telegram bot",
    )
    async def tg_send_video(
        video: str = Field(description="Video URL"),
        cover: str = Field("", description="Cover for the video in the message. Optional"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Video caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
    ):
        res = await bot.send_video(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            video=video,
            cover=cover or None,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
        )
        return res.to_json()


    @mcp.tool(
        description="Send audio via telegram bot",
    )
    async def tg_send_audio(
        audio: str = Field(description="Audio URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="Audio caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
    ):
        res = await bot.send_audio(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            audio=audio,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
        )
        return res.to_json()


    @mcp.tool(
        description="Send general files via telegram bot",
    )
    async def tg_send_file(
        url: str = Field(description="File URL"),
        chat_id: str = Field("", description="Telegram chat id, Default to get from environment variables"),
        caption: str = Field("", description="File caption, 0-1024 characters after entities parsing"),
        parse_mode: str = Field("", description=f"Mode for parsing entities in the caption. [text/MarkdownV2]"),
    ):
        res = await bot.send_document(
            chat_id=chat_id or TELEGRAM_DEFAULT_CHAT,
            document=url,
            caption=caption or None,
            parse_mode=parse_mode if parse_mode in [TELEGRAM_MARKDOWN_V2] else None,
        )
        return res.to_json()


    @mcp.tool(
        description="Telegram supports Markdown formatting. Must use this tool before sending markdown to Telegram.",
    )
    def tg_markdown_rule():
        return TELEGRAM_MARKDOWN_RULE
