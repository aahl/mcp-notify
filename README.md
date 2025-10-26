# 💬 Notify MCP Server

[![smithery badge](https://smithery.ai/badge/@aahl/mcp-notify)](https://smithery.ai/server/@aahl/mcp-notify)
<!-- mcp-name: io.github.aahl/mcp-notify -->

提供消息推送的 MCP (Model Context Protocol) 服务器，支持企业微信、钉钉机器人、Telegram、Bark


## 安装

### Installing via Smithery

To install Notify MCP Server automatically via [Smithery](https://smithery.ai/server/@aahl/mcp-notify):

```bash
npx -y @smithery/cli install @aahl/mcp-notify
```

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

### 方式2: Docker
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


## 相关连接
- [大饼报告](https://t.me/s/mcpBtc) - 基于此MCP实现的Telegram频道
