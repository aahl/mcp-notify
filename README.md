# 💬 Notify MCP Server

<!-- mcp-name: io.github.aahl/mcp-notify -->

提供消息推送的 MCP (Model Context Protocol) 服务器，支持企业微信、钉钉机器人、Telegram、Bark


## 安装

### 方式1: uvx
```yaml
{
  "mcpServers": {
    "mcp-notify": {
      "command": "uvx",
      "args": ["mcp-notify"],
      "env": {
        "WEWORK_BOT_KEY": "your-wework-bot-key", # 企业微信群机器人key，也可以在提示词指定
        "WEWORK_APP_CORPID": "ww0123456789abcd", # 企业微信所属的企业ID
        "WEWORK_APP_SECRET": "Your-Secret-Key",  # 企业微信应用的凭证密钥
        "WEWORK_APP_AGENTID": "1000002",         # 企业微信应用的ID
        "WEWORK_APP_TOUSER": "admin",            # 企业微信默认接收人ID
        "WEWORK_BASE_URL": "https://qyapi.weixin.qq.com", # 企业微信API反代理地址，用于可信IP
        "DINGTALK_BOT_KEY": "your-dingtalk-bot", # 钉钉群机器人access_token
        "BARK_DEVICE_KEY": "your-bark-key",      # Bark device key
        "TELEGRAM_DEFAULT_CHAT": "-10000000000", # Telegram Default Chat ID
        "TELEGRAM_BOT_TOKEN": "123456789:ABCDE", # Telegram Bot Token
        "TELEGRAM_BASE_URL": "https://api.telegram.org", # Optional
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
      "url": "https://server.smithery.ai/@aahl/mcp-notify/mcp" # Streamable HTTP
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
      "url": "http://0.0.0.0:8809/mcp" # Streamable HTTP
    }
  }
}
```

### 快速开始
- 在线体验: [![smithery.ai](https://smithery.ai/badge/@aahl/mcp-notify)](https://smithery.ai/server/@aahl/mcp-notify)
- 添加到 Cursor [![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/zh/install-mcp?name=notify&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19)
- 添加到 VS Code [![Install MCP Server](https://img.shields.io/badge/VS_Code-+?label=Add+MCP+Server&color=0098FF)](https://insiders.vscode.dev/redirect?url=vscode:mcp/install%3F%7B%22name%22%3A%22notify%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-notify%22%5D%7D)
- 添加到 Cherry Studio [![Install MCP Server](https://img.shields.io/badge/Cherry_Studio-+?label=Add+MCP+Server&color=FF5F5F)](https://gitee.com/link?target=cherrystudio%3A%2F%2Fmcp%2Finstall%3Fservers%3DeyJtY3BTZXJ2ZXJzIjp7Im5vdGlmeSI6eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtY3Atbm90aWZ5Il19fX0%3D)
- 添加到 Claude Code, 执行命令: `claude mcp add notify -- uvx mcp-notify`
- 添加到 OpenAI CodeX, 执行命令: `codex mcp add notify -- uvx mcp-notify`

------

## 相关连接
- [大饼报告](https://t.me/s/mcpBtc) - 基于此MCP实现的Telegram频道
