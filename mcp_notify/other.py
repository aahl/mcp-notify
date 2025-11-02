import os
import logging
import requests
from fastmcp import FastMCP
from pydantic import Field

_LOGGER = logging.getLogger(__name__)

NTFY_ACTIONS_RULE = """
The following actions are supported:
- view: Opens a website or app when the action button is tapped
- broadcast: Sends an Android broadcast intent when the action button is tapped (only supported on Android)
- http: Sends HTTP POST/GET/PUT request when the action button is tapped
```json
[
  {
    "action": "view",
    "label": "Open portal",
    "url": "https://home.nest.com/",
    "clear": true
  },
  {
    "action": "http",
    "label": "Turn down",
    "url": "https://api.nest.com/",
    "body": "{\"temperature\": 65}"
  },
  {
    "action": "broadcast",
    "label": "Take picture",
    "extras": {
        "cmd": "pic",
        "camera": "front"
    }
  }
]
```
"""


def add_tools(mcp: FastMCP):

    @mcp.tool(
        title="钉钉群机器人-发送文本消息",
        description="钉钉群机器人发送文本或Markdown消息",
    )
    def ding_send_text(
        text: str = Field(description="消息内容"),
        title: str = Field("", description="消息标题"),
        msgtype: str = Field("markdown", description="内容类型，仅支持: text/markdown"),
        bot_key: str = Field("", description="钉钉群机器人access_token，默认从环境变量获取"),
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
        title="飞书/Lark机器人-发送文本消息",
        description="飞书/Lark群机器人发送文本或Markdown消息",
    )
    def lark_send_text(
        text: str = Field(description="消息内容"),
        msgtype: str = Field("markdown", description="内容类型，仅支持: text/markdown"),
        bot_key: str = Field("", description="飞书/Lark机器人key，uuid格式，默认从环境变量获取"),
        is_lark: int = Field(0, description="根据用户描述识别 0:飞书 1:Lark"),
    ):
        """
        https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
        https://open.larksuite.com/document/client-docs/bot-v3/add-custom-bot
        """
        if msgtype == "markdown":
            body = {
                "msg_type": "interactive",
                "card": {"elements": [{"tag": msgtype, "content": text}]},
            }
        else:
            body = {"msg_type": msgtype, "content": {"text": text}}
        if not bot_key:
            bot_key = os.getenv("LARK_BOT_KEY" if is_lark else "FEISHU_BOT_KEY", "")
        if is_lark:
            base = os.getenv("LARK_BASE_URL") or "https://open.larksuite.com"
        else:
            base = os.getenv("FEISHU_BASE_URL") or "https://open.feishu.cn"
        res = requests.post(
            f"{base}/open-apis/bot/v2/hook/{bot_key}",
            json=body,
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
                "volume": volume,
            },
        )
        return res.json()


    @mcp.tool(
        title="Ntfy Push Notification",
        description="Push a notification via Ntfy",
    )
    def ntfy_send_notify(
        message: str = Field(description="Notification message body; set to `triggered` if empty or not passed"),
        title: str = Field("", description="Notification title"),
        topic: str = Field("", description="Target topic name or URL"),
        click: str = Field("", description="URL opened when notification is clicked"),
        attach: str = Field("", description="URL of an attachment"),
        icon: str = Field("", description="URL of notification icon"),
        markdown: bool = Field(False, description="Set to `true` if the message is Markdown-formatted"),
        filename: str = Field("", description="File name of the attachment"),
        priority: int = Field(3, description="Message priority with 1=min, 3=default and 5=max"),
        delay: str = Field("", description="Timestamp or duration for delayed delivery. Example: 30min, 9am"),
        actions: list | None = Field(None, description=f"List of action buttons.{NTFY_ACTIONS_RULE}"),
    ):
        """
        https://docs.ntfy.sh/publish/#publish-as-json
        """
        base = os.getenv("NTFY_BASE_URL") or "https://ntfy.sh"
        if topic and topic.startswith("http"):
            base, topic = topic.rsplit("/", 1)
        if not topic:
            topic = os.getenv("NTFY_DEFAULT_TOPIC", "")
        data = {
            "topic": topic,
            "title": title,
            "message": message,
            "click": click,
            "icon": icon,
            "markdown": markdown or False,
            "priority": priority,
            "delay": delay,
        }
        if attach:
            data["attach"] = attach
            data["filename"] = filename
        if actions:
            data["actions"] = actions
        res = requests.post(f"{base}", json=data)
        return res.json()
