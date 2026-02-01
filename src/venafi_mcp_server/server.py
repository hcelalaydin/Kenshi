import sys
import asyncio
import logging
import importlib
import pkgutil

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from venafi_mcp_server.registry import registry
import venafi_mcp_server.tools

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("venafi-mcp-server")

server = Server("venafi-mcp-server")

def load_tools():
    # Dynamically import all modules in the tools package
    package = venafi_mcp_server.tools
    prefix = package.__name__ + "."
    for _, name, _ in pkgutil.iter_modules(package.__path__, prefix):
        try:
            importlib.import_module(name)
            logger.info(f"Loaded tool module: {name}")
        except Exception as e:
            logger.error(f"Failed to load tool module {name}: {e}")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return registry.get_tools()

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        return await registry.call_tool(name, arguments)
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]

async def main():
    load_tools()
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
