import os
import logging
import requests
from fastmcp import FastMCP
from pydantic import Field

_LOGGER = logging.getLogger(__name__)


def add_tools(mcp: FastMCP):

    @mcp.tool(
        title="钉钉群机器人-发送文本消息",
        description="钉钉群机器人发送文本或Markdown消息",
    )
    def ding_send_text(
        text: str = Field(description="消息内容"),
        title: str = Field("", description="消息标题"),
        msgtype: str = Field("markdown", description="内容类型，仅支持: text/markdown"),
        bot_key: str = Field("", description="钉钉群机器人access_token，uuid格式，默认从环境变量获取"),
    ):
        """
        https://open.dingtalk.com/document/development/custom-robots-send-group-messages
        """
        if msgtype == "markdown":
            body = {"title": title, "text": text}
        else:
            body = {"content": f'{title}\n{text}'.strip()}
        if not bot_key:
            bot_key = os.getenv("DINGTALK_BOT_KEY", "")
        base = os.getenv("DINGTALK_BASE_URL") or "https://oapi.dingtalk.com"
        res = requests.post(
            f"{base}/robot/send?access_token={bot_key}",
            json={"msgtype": msgtype, msgtype: body},
        )
        return res.json()


    @mcp.tool(
        title="Bark推送通知",
        description="通过Bark推送通知",
    )
    def bark_send_notify(
        body: str = Field(description="推送内容"),
        title: str = Field("", description="推送标题"),
        subtitle: str = Field("", description="推送副标题"),
        device_key: str = Field("", description="设备key，默认从环境变量获取"),
        url: str = Field("", description="点击推送时，跳转的URL ，支持URL Scheme 和 Universal Link"),
        icon: str = Field("", description="自定义图标URL"),
        level: str = Field(
            "active",
            description="推送中断级别。"
                        "critical: 重要警告, 在静音模式下也会响铃"
                        "active：默认值，系统会立即亮屏显示通知"
                        "timeSensitive：时效性通知，可在专注状态下显示通知。"
                        "passive：仅将通知添加到通知列表，不会亮屏提醒。",
        ),
        volume: int = Field(5, description="重要警告的通知音量(0-10)，默认为5"),
    ):
        """
        https://bark.day.app/#/tutorial
        """
        if not device_key:
            device_key = os.getenv("BARK_DEVICE_KEY", "")
        base = os.getenv("BARK_BASE_URL") or "https://api.day.app"
        res = requests.post(
            f"{base}/{device_key}",
            json={
                "body": body,
                "title": title,
                "subtitle": subtitle,
                "url": url,
                "icon": icon,
                "level": level,
            },
        )
        return res.json()
