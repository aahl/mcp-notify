[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/aahl-mcp-notify-badge.png)](https://mseep.ai/app/aahl-mcp-notify)

# 💬 Notify MCP Server

<!-- mcp-name: io.github.aahl/mcp-notify -->
<!-- [![MCP Badge](https://lobehub.com/badge/mcp/aahl-mcp-notify)](https://lobehub.com/mcp/aahl-mcp-notify) -->

简体中文 | [English](https://github.com/aahl/mcp-notify/blob/main/README_en.md)

提供消息推送的 MCP (Model Context Protocol) 服务器，支持企业微信、钉钉、Telegram、Bark、Lark、飞书、Home Assistant


## 安装

### 方式1: uvx
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

### 方式2: [Smithery](https://smithery.ai/server/@aahl/mcp-notify)
> 需要通过OAuth授权或Smithery key

```yaml
{
  "mcpServers": {
    "mcp-aktools": {
      "url": "https://server.smithery.ai/@aahl/mcp-notify/mcp" # 流式传输HTTP
    }
  }
}
```

### 方式3: Docker
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
      "url": "http://0.0.0.0:8809/mcp" # 流式传输HTTP
    }
  }
}
```

### 快速开始
- 在线体验: [![fastmcp.cloud](https://img.shields.io/badge/Cloud-+?label=FastMCP)](https://fastmcp.cloud/xiaomi/notify/chat)
- 在线体验: [![smithery.ai](https://smithery.ai/badge/@aahl/mcp-notify)](https://smithery.ai/server/@aahl/mcp-notify)
- 添加到 Cursor [![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/zh/install-mcp?name=notify&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19)
- 添加到 VS Code [![Install MCP Server](https://img.shields.io/badge/VS_Code-+?label=Add+MCP+Server&color=0098FF)](https://insiders.vscode.dev/redirect?url=vscode:mcp/install%3F%7B%22name%22%3A%22notify%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-notify%22%5D%7D)
- 添加到 Cherry Studio [![Install MCP Server](https://img.shields.io/badge/Cherry_Studio-+?label=Add+MCP+Server&color=FF5F5F)](https://gitee.com/link?target=cherrystudio%3A%2F%2Fmcp%2Finstall%3Fservers%3DeyJtY3BTZXJ2ZXJzIjp7Im5vdGlmeSI6eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19fX0%3D)
- 添加到 Claude Code, 执行命令: `claude mcp add notify -- uvx mcp-notify`
- 添加到 OpenAI CodeX, 执行命令: `codex mcp add notify -- uvx mcp-notify`


### ⚙️ 环境变量

#### 企业微信群机器人
- `WEWORK_BOT_KEY`: 企业微信群机器人默认key，也可以在提示词指定

#### 企业微信应用号
- `WEWORK_APP_CORPID`: 企业微信所属的企业ID
- `WEWORK_APP_SECRET`: 企业微信应用的凭证密钥
- `WEWORK_APP_AGENTID`: 企业微信应用的ID，默认: `1000002`
- `WEWORK_APP_TOUSER`: 企业微信默认接收人ID，也可以在提示词指定，默认: `@all`
- `WEWORK_BASE_URL`: 企业微信API反代理地址，用于可信IP，默认: `https://qyapi.weixin.qq.com`

#### 钉钉群机器人
- `DINGTALK_BOT_KEY`: 钉钉群机器人access_token
- `DINGTALK_BASE_URL`: 钉钉API地址，默认: `https://oapi.dingtalk.com`

#### 飞书/Lark群机器人
- `FEISHU_BOT_KEY`: 飞书群机器人key，也可以在提示词指定
- `FEISHU_BASE_URL`: 飞书API地址，默认: `https://open.feishu.cn`
- `LARK_BOT_KEY`: Lark群机器人key，也可以在提示词指定
- `LARK_BASE_URL`: Lark API地址，默认: `https://open.larksuite.com`

#### Telegram
- `TELEGRAM_DEFAULT_CHAT`: Telegram 默认会话ID，也可以在提示词指定
- `TELEGRAM_BOT_TOKEN`: Telegram 机器人令牌
- `TELEGRAM_BASE_URL`: Telegram API反代理地址，默认: `https://api.telegram.org`

#### Home Assistant
- `HASS_BASE_URL`: Home Assistant 地址，默认: `http://homeassistant.local:8123`
- `HASS_ACCESS_TOKEN`: Home Assistant 长效令牌
- `HASS_MOBILE_KEY`: Home Assistant 移动设备key (如: mobile_app_your_iphone)，也可在提示词指定

#### 其他
- `BARK_DEVICE_KEY`: 默认Bark设备key，也可以在提示词指定
- `BARK_BASE_URL`: Bark API地址，默认: `https://api.day.app`
- `NTFY_DEFAULT_TOPIC`: 默认Ntfy订阅主题，也可以在提示词指定
- `NTFY_BASE_URL`: Ntfy API地址，默认: `https://ntfy.sh`
- `PUSH_PLUS_TOKEN`: 默认PushPlus令牌，也可以在提示词指定
- `PUSH_PLUS_BASE_URL`: PushPlus API地址，默认: `http://www.pushplus.plus`

------

## 🛠️ 可用工具

<details>
<summary><strong>企业微信群机器人</strong></summary>

- `wework_send_text` - 发送文本或Markdown消息
- `wework_send_image` - 发送图片消息
- `wework_send_news` - 发送图文链接消息

</details>

<details>
<summary><strong>企业微信应用号</strong></summary>

- `wework_app_send_text` - 发送文本或Markdown消息
- `wework_app_send_image` - 发送图片消息
- `wework_app_send_video` - 发送视频消息
- `wework_app_send_voice` - 发送语音消息
- `wework_app_send_file` - 发送文件消息
- `wework_app_send_news` - 发送图文链接消息

</details>

<details>
<summary><strong>Telegram Bot</strong></summary>

- `tg_send_message` - 发送文本或Markdown消息
- `tg_send_photo` - 发送图片消息
- `tg_send_video` - 发送视频消息
- `tg_send_audio` - 发送音频消息
- `tg_send_file` - 发送文件消息

</details>

<details>
<summary><strong>其他工具</strong></summary>

- `ding_send_text` - 通过钉钉群机器人发送文本或Markdown消息
- `lark_send_text` - 通过飞书/Lark群机器人发送文本或Markdown消息
- `bark_send_notify` - 通过Bark发送通知
- `ntfy_send_notify` - 通过Ntfy发送通知
- `pushplus_send_msg` - 通过PushPlus发送消息
- `ha_send_mobile` - 通过Home Assistant发送通知
- `text_to_sound` - 将一段文本转成mp3音频链接

</details>


------

## 🔗 相关连接
- [大饼报告](https://t.me/s/mcpBtc) - 基于此MCP实现的Telegram频道
- https://github.com/hasscc/ai-conversation/discussions/3
- https://linux.do/t/topic/1098688

------

<a href="https://glama.ai/mcp/servers/@al-one/mcp-notify">
  <img width="400" src="https://glama.ai/mcp/servers/@al-one/mcp-notify/badge">
</a>
