import json
import mcp.types as types
from venafi_mcp_server.registry import registry
from venafi_mcp_server.client import get_tpp_client

@registry.register(
    types.Tool(
        name="get_identity_self",
        description="Get information about the current authenticated user.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
)
async def get_identity_self(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    response = tpp.api.websdk.Identity.Self.get()
    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="browse_identities",
        description="Search for identities (users/groups).",
        inputSchema={
            "type": "object",
            "properties": {
                "filter": {"type": "string", "description": "Search filter string"},
                "limit": {"type": "integer", "default": 10},
                "identity_type": {"type": "integer", "description": "0=All, 1=User, 2=Group", "default": 0}
            },
            "required": ["filter"]
        }
    )
)
async def browse_identities(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    filter_str = arguments.get("filter")
    limit = arguments.get("limit", 10)
    identity_type = arguments.get("identity_type", 0)

    response = tpp.api.websdk.Identity.Browse.post(
        filter=filter_str,
        limit=limit,
        identity_type=identity_type
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]
