import os
import io
import logging
import requests
import hashlib
import base64
from fastmcp import FastMCP
from pydantic import Field
from cachetools import cached, TTLCache

_LOGGER = logging.getLogger(__name__)

WEWORK_BOT_KEY = os.getenv("WEWORK_BOT_KEY", "")
WEWORK_APP_AGENTID = int(os.getenv("WEWORK_APP_AGENTID", 1000002))
WEWORK_APP_CORPID = os.getenv("WEWORK_APP_CORPID", "")
WEWORK_APP_SECRET = os.getenv("WEWORK_APP_SECRET", "")
WEWORK_APP_TOUSER = os.getenv("WEWORK_APP_TOUSER", "@all")
WEWORK_BASE_URL = os.getenv("WEWORK_BASE_URL") or "https://qyapi.weixin.qq.com"

FIELD_BOT_KEY = Field("", description="企业微信群机器人key，uuid格式，默认从环境变量获取")
FIELD_TO_USER = Field("", description="接收消息的成员ID，多个用`|`分隔，为`@all`时向该企业应用全部成员发送，默认从环境变量获取")


def add_tools(mcp: FastMCP):

    @mcp.tool(
        title="企业微信群机器人-发送文本消息",
        description="通过企业微信群机器人发送文本或Markdown消息",
    )
    def wework_send_text(
        text: str = Field(description="消息内容，长度限制: (text: 2048个字节, markdown_v2: 4096个字节)"),
        msgtype: str = Field("text", description="内容类型，仅支持: text/markdown_v2"),
        bot_key: str = FIELD_BOT_KEY,
    ):
        if msgtype == "markdown":
            msgtype = "markdown_v2"
        res = requests.post(
            f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key or WEWORK_BOT_KEY}",
            json={"msgtype": msgtype, msgtype: {"content": text}},
        )
        return res.json()


    @mcp.tool(
        title="企业微信群机器人-发送图片消息",
        description="通过企业微信群机器人发送图片消息",
    )
    def wework_send_image(
        url: str = Field(description="图片url"),
        bot_key: str = FIELD_BOT_KEY,
    ):
        res = requests.get(url, timeout=120)
        res.raise_for_status()
        b64str = base64.b64encode(res.content).decode()
        md5str = hashlib.md5(res.content).hexdigest()
        res = requests.post(
            f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key or WEWORK_BOT_KEY}",
            json={"msgtype": "image", "image": {"base64": b64str, "md5": md5str}},
            timeout=120,
        )
        return res.json()


    @mcp.tool(
        title="企业微信群机器人-发送图文消息",
        description="通过企业微信群机器人发送图文链接消息",
    )
    def wework_send_news(
        title: str = Field(description="标题，不超过128个字节"),
        url: str = Field(description="跳转链接，必填"),
        picurl: str = Field("", description="图片URL"),
        description: str = Field("", description="描述，不超过512个字节"),
        bot_key: str = FIELD_BOT_KEY,
    ):
        res = requests.post(
            f"{WEWORK_BASE_URL}/cgi-bin/webhook/send?key={bot_key or WEWORK_BOT_KEY}",
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


    if WEWORK_APP_CORPID and WEWORK_APP_SECRET:
        @cached(TTLCache(maxsize=1, ttl=3600))
        def get_access_token():
            res = requests.get(
                f"{WEWORK_BASE_URL}/cgi-bin/gettoken",
                params={"corpid": WEWORK_APP_CORPID, "corpsecret": WEWORK_APP_SECRET},
                timeout=60,
            )
            return res.json().get("access_token")


        @mcp.tool(
            title="企业微信应用号-发送文本消息",
            description="通过企业微信应用号发送文本或Markdown消息",
        )
        def wework_app_send_text(
            text: str = Field(description="消息内容，最长不超过2048个字节"),
            msgtype: str = Field("text", description="内容类型，仅支持: text/markdown"),
            touser: str = FIELD_TO_USER,
        ):
            res = requests.post(
                f"{WEWORK_BASE_URL}/cgi-bin/message/send?access_token={get_access_token()}",
                json={
                    "touser": touser or WEWORK_APP_TOUSER,
                    "agentid": WEWORK_APP_AGENTID,
                    "msgtype": msgtype,
                    msgtype: {"content": text},
                    "enable_duplicate_check": 1,
                    "duplicate_check_interval": 60,
                },
            )
            return res.json() or {}

        @mcp.tool(
            title="企业微信应用号-发送图片消息",
            description="通过企业微信应用号发送发送图片消息",
        )
        def wework_app_send_image(
            url: str = Field(description="图片URL"),
            touser: str = FIELD_TO_USER,
        ):
            return wework_send_media(touser, url, "image")

        @mcp.tool(
            title="企业微信应用号-发送视频消息",
            description="通过企业微信应用号发送发送视频消息",
        )
        def wework_app_send_video(
            url: str = Field(description="视频URL"),
            touser: str = FIELD_TO_USER,
        ):
            return wework_send_media(touser, url, "video")

        @mcp.tool(
            title="企业微信应用号-发送语音消息",
            description="通过企业微信应用号发送发送语音消息",
        )
        def wework_app_send_voice(
            url: str = Field(description="语音URL"),
            touser: str = FIELD_TO_USER,
        ):
            return wework_send_media(touser, url, "voice")

        @mcp.tool(
            title="企业微信应用号-发送文件消息",
            description="通过企业微信应用号发送发送文件消息",
        )
        def wework_app_send_file(
            url: str = Field(description="文件URL"),
            touser: str = FIELD_TO_USER,
        ):
            return wework_send_media(touser, url, "file")

        def wework_send_media(touser, url: str, msgtype=None):
            if msgtype:
                pass
            elif '.jpg' in url.lower() or '.jpeg' in url.lower() or '.png' in url.lower():
                msgtype = 'image'
            elif '.mp4' in url.lower():
                msgtype = 'video'
            elif '.arm' in url.lower():
                msgtype = 'voice'
            else:
                msgtype = 'file'
            res = requests.get(url, timeout=120)
            res.raise_for_status()
            file = io.BytesIO(res.content)
            mine = res.headers.get("content-type") or "application/octet-stream"
            res = requests.post(
                f"{WEWORK_BASE_URL}/cgi-bin/media/upload",
                params={"type": msgtype, "access_token": get_access_token()},
                files={"media": ("filename", file, mine)},
                timeout=120,
            )
            media = res.json() or {}
            if not (media_id := media.get("media_id")):
                return media
            res = requests.post(
                f"{WEWORK_BASE_URL}/cgi-bin/message/send?access_token={get_access_token()}",
                json={
                    "touser": touser or WEWORK_APP_TOUSER,
                    "agentid": WEWORK_APP_AGENTID,
                    "msgtype": msgtype,
                    msgtype: {"media_id": media_id},
                },
            )
            return res.json()


        @mcp.tool(
            title="企业微信应用号-发送图文卡片消息",
            description="通过企业微信应用号发送图文卡片消息",
        )
        def wework_app_send_news(
            title: str = Field(description="标题，不超过128个字符"),
            url: str = Field(description="跳转链接，最长2048字节，必须包含协议头(http/https)"),
            picurl: str = Field("", description="图片URL"),
            description: str = Field("", description="描述，不超过512个字符"),
            touser: str = FIELD_TO_USER,
        ):
            res = requests.post(
                f"{WEWORK_BASE_URL}/cgi-bin/message/send?access_token={get_access_token()}",
                json={
                    "touser": touser or WEWORK_APP_TOUSER,
                    "agentid": WEWORK_APP_AGENTID,
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
            return res.json() or {}
