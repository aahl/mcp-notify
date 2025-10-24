# 💬 Notify MCP Server

<!-- mcp-name: io.github.aahl/mcp-notify -->

提供消息推送的 MCP (Model Context Protocol) 服务器


## 安装

### 方式1: uvx
```yaml
{
  "mcpServers": {
    "mcp-notify": {
      "command": "uvx",
      "args": ["mcp-notify"],
      "env": {
        "WEWORK_BOT_KEY": "your-wework-bot-key" # 企业微信群机器人key
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
