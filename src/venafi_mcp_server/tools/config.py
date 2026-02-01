import json
import mcp.types as types
from venafi_mcp_server.registry import registry
from venafi_mcp_server.client import get_tpp_client

@registry.register(
    types.Tool(
        name="list_objects",
        description="Find Config objects matching a pattern.",
        inputSchema={
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "The search pattern (e.g. \\VED\\Policy\\*)"},
                "class_name": {"type": "string", "description": "Filter by class name (e.g. X509 Certificate)"},
                "recursive": {"type": "boolean", "default": False}
            },
            "required": ["pattern"]
        }
    )
)
async def list_objects(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    pattern = arguments.get("pattern")
    class_name = arguments.get("class_name")
    recursive = arguments.get("recursive", False)

    if class_name:
        response = tpp.api.websdk.Config.FindObjectsOfClass.post(
            class_name=class_name,
            pattern=pattern,
            recursive=recursive
        )
    else:
        response = tpp.api.websdk.Config.Find.post(pattern=pattern)

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="read_object",
        description="Read all attributes of a Config object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_dn": {"type": "string", "description": "The DN of the object"}
            },
            "required": ["object_dn"]
        }
    )
)
async def read_object(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    object_dn = arguments.get("object_dn")

    response = tpp.api.websdk.Config.ReadAll.post(object_dn=object_dn)

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="write_object_attribute",
        description="Write a specific attribute to a Config object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_dn": {"type": "string", "description": "The DN of the object"},
                "attribute_name": {"type": "string", "description": "The name of the attribute (e.g. Contact)"},
                "values": {"type": "array", "items": {"type": "string"}, "description": "List of values"}
            },
            "required": ["object_dn", "attribute_name", "values"]
        }
    )
)
async def write_object_attribute(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    object_dn = arguments.get("object_dn")
    attribute_name = arguments.get("attribute_name")
    values = arguments.get("values")

    response = tpp.api.websdk.Config.WriteDn.post(
        object_dn=object_dn,
        attribute_name=attribute_name,
        values=values
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="create_object",
        description="Create a new Config object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_dn": {"type": "string", "description": "The DN of the new object"},
                "class_name": {"type": "string", "description": "The Class Name (e.g. Device)"}
            },
            "required": ["object_dn", "class_name"]
        }
    )
)
async def create_object(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    object_dn = arguments.get("object_dn")
    class_name = arguments.get("class_name")

    response = tpp.api.websdk.Config.Create.post(
        object_dn=object_dn,
        class_name=class_name,
        name_attribute_list=[]
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="delete_object",
        description="Delete a Config object.",
        inputSchema={
            "type": "object",
            "properties": {
                "object_dn": {"type": "string", "description": "The DN of the object to delete"},
                "recursive": {"type": "boolean", "default": False}
            },
            "required": ["object_dn"]
        }
    )
)
async def delete_object(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    object_dn = arguments.get("object_dn")
    recursive = arguments.get("recursive", False)

    response = tpp.api.websdk.Config.Delete.post(
        object_dn=object_dn,
        recursive=recursive
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]
