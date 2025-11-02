import os
import logging
import argparse
from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

from . import (
    wework,
    tgbot,
    other,
    hass,
    util,
)

_LOGGER = logging.getLogger(__name__)


mcp = FastMCP(name="mcp-notify", version="0.1.4")
wework.add_tools(mcp)
tgbot.add_tools(mcp)
other.add_tools(mcp)
hass.add_tools(mcp)
util.add_tools(mcp)


def main():
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
