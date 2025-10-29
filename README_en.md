# 💬 Notify MCP Server

English | [简体中文](https://github.com/aahl/mcp-notify/blob/main/README.md)

Provides an MCP (Model Context Protocol) server for message push, supporting WeWork, DingTalk, Telegram, Bark, Lark, Feishu, and Home Assistant.


## Install

### Method 1: uvx
```yaml
{
  "mcpServers": {
    "mcp-notify": {
      "command": "uvx",
      "args": ["mcp-notify"],
      "env": {
        "WEWORK_BOT_KEY": "your-wework-bot-key"
      }
    }
  }
}
```

### Method 2: [Smithery](https://smithery.ai/server/@aahl/mcp-notify)
> Requires OAuth authorization or a Smithery key

```yaml
{
  "mcpServers": {
    "mcp-aktools": {
      "url": "https://server.smithery.ai/@aahl/mcp-notify/mcp" # Streamable HTTP
    }
  }
}
```

### Method 3: Docker
```bash
mkdir /opt/mcp-notify
cd /opt/mcp-notify
wget https://raw.githubusercontent.com/aahl/mcp-notify/refs/heads/main/docker-compose.yml
docker-compose up -d
```
```yaml
{
  "mcpServers": {
    "mcp-notify": {
      "url": "http://0.0.0.0:8809/mcp" # Streamable HTTP
    }
  }
}
```

### Get Started
- Online Experience: [![fastmcp.cloud](https://img.shields.io/badge/Cloud-+?label=FastMCP)](https://fastmcp.cloud/xiaomi/notify/chat)
- Online Experience: [![smithery.ai](https://smithery.ai/badge/@aahl/mcp-notify)](https://smithery.ai/server/@aahl/mcp-notify)
- Add to Cursor [![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/zh/install-mcp?name=notify&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19)
- Add to VS Code [![Install MCP Server](https://img.shields.io/badge/VS_Code-+?label=Add+MCP+Server&color=0098FF)](https://insiders.vscode.dev/redirect?url=vscode:mcp/install%3F%7B%22name%22%3A%22notify%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-notify%22%5D%7D)
- Add to Cherry Studio [![Install MCP Server](https://img.shields.io/badge/Cherry_Studio-+?label=Add+MCP+Server&color=FF5F5F)](https://gitee.com/link?target=cherrystudio%3A%2F%2Fmcp%2Finstall%3Fservers%3DeyJtY3BTZXJ2ZXJzIjp7Im5vdGlmeSI6eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19fX0%3D)
- Add to Claude Code, Exec shell: `claude mcp add notify -- uvx mcp-notify`
- Add to OpenAI CodeX, Exec shell: `codex mcp add notify -- uvx mcp-notify`


### ⚙️ Environment variables

#### WeWork Group Robot
- `WEWORK_BOT_KEY`: The default key for the WeWork group robot can also be specified in the prompt.

#### WeWork Application
- `WEWORK_APP_CORPID`: Company ID of WeWork
- `WEWORK_APP_SECRET`: Secret key of WeWork
- `WEWORK_APP_AGENTID`: Agent ID of WeWork Application, Default: `1000002`
- `WEWORK_APP_TOUSER`: Default recipient user ID in WeWork, Default: `@all`
- `WEWORK_BASE_URL`: WeWork API reverse proxy address for trusted IPs, Default: `https://qyapi.weixin.qq.com`

#### DingTalk Robot
- `DINGTALK_BOT_KEY`: Access token of DingTalk Robot, Can also be specified in the prompt
- `DINGTALK_BASE_URL`: API address of DingTalk, Default: `https://oapi.dingtalk.com`

#### Lark/Feishu Robot
- `LARK_BOT_KEY`: The key of Lark Robot
- `LARK_BASE_URL`: API address of Lark, Default: `https://open.larksuite.com`
- `FEISHU_BOT_KEY`: The key of Feishu Robot
- `FEISHU_BASE_URL`: API address of Feishu, Default: `https://open.feishu.cn`

#### Bark
- `BARK_DEVICE_KEY`: Bark device key, Can also be specified in the prompt
- `BARK_BASE_URL`: Bark Base URL, Default: `https://api.day.app`

#### Telegram
- `TELEGRAM_DEFAULT_CHAT`: Telegram Default Chat ID, Can also be specified in the prompt
- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token
- `TELEGRAM_BASE_URL`: Telegram Base URL, Default: `https://api.telegram.org`

#### Home Assistant
- `HASS_BASE_URL`: Home Assistant Base URL, Default: `http://homeassistant.local:8123`
- `HASS_ACCESS_TOKEN`: Home Assistant Long-Lived Access Token
- `HASS_MOBILE_KEY`: Home Assistant Mobile Device Key, Can also be specified in the prompt

------

## 🛠️ Available Tools

<details>
<summary><strong>WeWork Group Robot</strong></summary>

- `wework_send_text` - Send text or markdown message
- `wework_send_image` - Send image message
- `wework_send_news` - Send news message

</details>

<details>
<summary><strong>WeWork Application</strong></summary>

- `wework_app_send_text` - Send text or markdown message
- `wework_app_send_image` - Send image message
- `wework_app_send_video` - Send video message
- `wework_app_send_voice` - Send voice message
- `wework_app_send_file` - Send file message
- `wework_app_send_news` - Send news message

</details>

<details>
<summary><strong>Telegram Bot</strong></summary>

- `tg_send_message` - Send text or markdown message
- `tg_send_photo` - Send image message
- `tg_send_video` - Send video message
- `tg_send_audio` - Send voice message
- `tg_send_file` - Send file message
- `tg_markdown_rule` - Telegram markdown rules

</details>

<details>
<summary><strong>Other Tools</strong></summary>

- `ding_send_text` - Sending text or markdown message via DingTalk group robot
- `lark_send_text` - Sending text or markdown message via Lark/Feishu group robot
- `bark_send_notify` - Send notification via Bark
- `ha_send_mobile` - Send notification via Home Assistant mobile APP
- `text_to_sound` - Convert a text segment into an audio link

</details>


------

## 🔗 Links
- [t.me/mcpBtc](https://t.me/s/mcpBtc) - A telegram channel based on this MCP implementation
- https://github.com/hasscc/ai-conversation/discussions/3
- https://linux.do/t/topic/1098688

------

<a href="https://glama.ai/mcp/servers/@al-one/mcp-notify">
  <img width="400" src="https://glama.ai/mcp/servers/@al-one/mcp-notify/badge">
</a>
