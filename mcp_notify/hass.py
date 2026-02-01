import os
import json

import requests
from fastmcp import FastMCP
from pydantic import Field

HA_NOTIFY_DATA_PROMPT = """
```json
{
  "image": "http://a.com/photo.jpg",
  "video": "http://a.com/video.mp4",
  "audio": "http://a.com/audio.mp3", # ios only
  "actions": [
    {
      "action": "YOUR_ACTION_KEY", # Required. The identifier passed back in events.
      "title": "Do Something",
      "icon": "sfsymbols:bell.slash" # ios only
    },
    {
      "action": "URL", # Must be set to URI if you plan to use a URI
      "title": "Open Url", # The action button title
      "url": "https://github.com" # URL to open when action is selected
    },
    {
      "action": "REPLY", # When set to REPLY, you will be prompted for text to send with the event.
      "title": "Reply me",
      "behavior": "textInput" # Optional. Set to `textInput` to prompt for text to return with the event. This also occurs when setting the action to `REPLY`.
    }
  ]
}
```
All fields in the extended data are optional.
"""

def add_tools(mcp: FastMCP, logger=None):

    @mcp.tool(
        title="Send to HomeAssistant Mobile APP",
        description="Send a notification to Home Assistant Mobile APP",
    )
    def ha_send_mobile(
        message: str = Field(description="Notification content"),
        title: str = Field("", description="Notification title"),
        subtitle: str = Field("", description="Notification subtitle"),
        data: str | dict = Field("{}", description=f"Extended data, json string.{HA_NOTIFY_DATA_PROMPT}"),
        url: str = Field("", description="Opening a URL when tapping on a notification"),
        device_key: str = Field("", description="Device key, Default to get from environment variables"),
    ):
        base = os.getenv("HASS_BASE_URL") or "http://homeassistant.local:8123"
        if not (token := os.getenv("HASS_ACCESS_TOKEN")):
            return "You need to set `HASS_ACCESS_TOKEN` in the environment variable"

        headers = {"Authorization": f"Bearer {token}"}
        if not device_key:
            device_key = os.getenv("HASS_MOBILE_KEY", "")
        if not device_key:
            res = requests.get(f"{base}/api/services", headers=headers)
            for service in res.json() or []:
                if service["domain"] != "notify":
                    continue
                for name in service["services"]:
                    if name.startswith("mobile_app_"):
                        device_key = name
                        break
        if device_key.startswith("notify."):
            device_key = device_key[7:]
        elif not device_key.startswith("mobile_app_"):
            device_key = f"mobile_app_{device_key}"

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError:
                data = {}
        elif not isinstance(data, dict):
            data = {}
        if url:
            data.setdefault("url", url)  # ios
            data.setdefault("clickAction", url)  # android
        if subtitle:
            data.setdefault("subtitle", subtitle)  # ios
            data.setdefault("subject", subtitle)  # android

        res = requests.post(
            f"{base}/api/services/notify/{device_key}",
            json={
                "message": message,
                "title": title,
                "data": data,
            },
            headers=headers,
        )
        return res.json()
