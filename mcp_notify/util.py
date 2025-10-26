from fastmcp import FastMCP
from pydantic import Field
from urllib.parse import urlencode


def add_tools(mcp: FastMCP):

    @mcp.tool(
        title="文本转音频",
        description="将一段文本转成mp3音频链接",
    )
    def text_to_sound(
        text: str = Field(description="文本内容"),
        lang: str = Field("en", description="目标语言，支持: en/zh/cte(粤语)/ara/de/fra/kor/pt/ru/spa/th, 建议根据文本内容选择"),
        speed: int = Field(7, description="语速，默认7"),
    ):
        if not text:
            return ""
        return 'https://fanyi.baidu.com/gettts?' + urlencode({
            'lan': lang,
            'spd': speed,
            'text': text,
            'source': 'web',
        })
