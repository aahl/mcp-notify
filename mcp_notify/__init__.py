import os
import logging
import argparse
import requests
import hashlib
import base64
from fastmcp import FastMCP
from pydantic import Field
from starlette.middleware.cors import CORSMiddleware

from .telegram import add_telegram_tools


_LOGGER = logging.getLogger(__name__)

mcp = FastMCP(name="mcp-notify")

WEWORK_BOT_KEY = os.getenv("WEWORK_BOT_KEY", "")
WEWORK_BASE_URL = os.getenv("WEWORK_BASE_URL") or "https://qyapi.weixin.qq.com"


@mcp.tool(
    title="企业微信群机器人-发送文本消息",
    description="通过企业微信群机器人发送文本或Markdown消息",
)
def wework_send_text(
    text: str = Field(description="消息内容，长度限制: (text: 2048个字节, markdown_v2: 4096个字节)"),
    msgtype: str = Field("text", description="内容类型，仅支持: text/markdown_v2"),
    bot_key: str = Field(WEWORK_BOT_KEY, description="机器人key，uuid格式"),
):
    if msgtype == "markdown":
        msgtype = "markdown_v2"
    res = requests.post(
        f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key}",
        json={"msgtype": msgtype, msgtype: {"content": text}},
    )
    return res.json()


@mcp.tool(
    title="企业微信群机器人-发送图片消息",
    description="通过企业微信群机器人发送图片消息",
)
def wework_send_image(
    url: str = Field(description="图片url"),
    bot_key: str = Field(WEWORK_BOT_KEY, description="机器人key，uuid格式"),
):
    res = requests.get(url, timeout=60)
    res.raise_for_status()
    b64str = base64.b64encode(res.content).decode()
    md5str = hashlib.md5(res.content).hexdigest()
    res = requests.post(
        f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key}",
        json={"msgtype": "image", "image": {"base64": b64str, "md5": md5str}},
    )
    return res.json()


@mcp.tool(
    title="企业微信群机器人-发送图文消息",
    description="通过企业微信群机器人发送图文链接消息",
)
def wework_send_news(
    title: str = Field(description="标题，不超过128个字节"),
    url: str = Field(description="跳转链接，必填"),
    picurl: str = Field("", description="图片url"),
    description: str = Field("", description="描述，不超过512个字节"),
    bot_key: str = Field(WEWORK_BOT_KEY, description="机器人key，uuid格式"),
):
    res = requests.post(
        f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key}",
        json={
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": description,
                        "url": url,
                        "picurl": picurl,
                    },
                ],
            },
        },
    )
    return res.json()


def main():
    add_telegram_tools(mcp)

    mode = os.getenv("TRANSPORT")
    port = int(os.getenv("PORT", 0)) or 80
    parser = argparse.ArgumentParser(description="Notify MCP Server")
    parser.add_argument("--http", action="store_true", help="Use streamable HTTP mode instead of stdio")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=port, help=f"Port to listen on (default: {port})")

    args = parser.parse_args()
    if args.http or mode == "http":
        app = mcp.streamable_http_app()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()

if __name__ == "__main__":
    main()
