import json
import mcp.types as types
from venafi_mcp_server.registry import registry
from venafi_mcp_server.client import get_tpp_client

@registry.register(
    types.Tool(
        name="query_logs",
        description="Query Venafi TPP logs.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 100},
                "offset": {"type": "integer", "default": 0},
                "from_time": {"type": "string", "description": "ISO 8601 format"},
                "to_time": {"type": "string", "description": "ISO 8601 format"},
                "component": {"type": "string"},
                "severity": {"type": "string"}
            }
        }
    )
)
async def query_logs(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()

    response = tpp.api.websdk.Log.get(
        limit=arguments.get("limit"),
        offset=arguments.get("offset"),
        from_time=arguments.get("from_time"),
        to_time=arguments.get("to_time"),
        component=arguments.get("component"),
        severity=arguments.get("severity")
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="write_log",
        description="Write a log entry.",
        inputSchema={
            "type": "object",
            "properties": {
                "component": {"type": "string"},
                "id": {"type": "integer", "description": "Event ID"},
                "severity": {"type": "integer"},
                "text1": {"type": "string"},
                "text2": {"type": "string"}
            },
            "required": ["component", "id"]
        }
    )
)
async def write_log(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()

    response = tpp.api.websdk.Log.post(
        component=arguments.get("component"),
        id=arguments.get("id"),
        severity=arguments.get("severity"),
        text1=arguments.get("text1"),
        text2=arguments.get("text2")
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]
