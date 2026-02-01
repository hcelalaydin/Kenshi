import mcp.types as types
from typing import Callable, Awaitable, List, Union

ToolHandler = Callable[[dict], Awaitable[List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]]]

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, types.Tool] = {}
        self.handlers: dict[str, ToolHandler] = {}

    def register(self, tool: types.Tool):
        def decorator(func: ToolHandler):
            self.tools[tool.name] = tool
            self.handlers[tool.name] = func
            return func
        return decorator

    def get_tools(self) -> List[types.Tool]:
        return list(self.tools.values())

    async def call_tool(self, name: str, arguments: dict) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        handler = self.handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")
        return await handler(arguments)

registry = ToolRegistry()
