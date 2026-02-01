import json
import mcp.types as types
from venafi_mcp_server.registry import registry
from venafi_mcp_server.client import get_tpp_client

@registry.register(
    types.Tool(
        name="request_ssh_certificate",
        description="Request an SSH certificate.",
        inputSchema={
            "type": "object",
            "properties": {
                "ca_dn": {"type": "string", "description": "The DN of the CA"},
                "key_id": {"type": "string", "description": "The Key ID"},
                "public_key_data": {"type": "string", "description": "The Public Key Data"},
                "policy_dn": {"type": "string", "description": "The Policy DN"},
                "principals": {"type": "array", "items": {"type": "string"}, "description": "List of principals"}
            },
            "required": ["ca_dn", "key_id"]
        }
    )
)
async def request_ssh_certificate(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    ca_dn = arguments.get("ca_dn")
    key_id = arguments.get("key_id")
    public_key_data = arguments.get("public_key_data")
    policy_dn = arguments.get("policy_dn")
    principals = arguments.get("principals")

    response = tpp.api.websdk.SSHCertificates.Request.post(
        ca_dn=ca_dn,
        key_id=key_id,
        public_key_data=public_key_data,
        policy_dn=policy_dn,
        principals=principals
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="retrieve_ssh_certificate",
        description="Retrieve an SSH certificate.",
        inputSchema={
            "type": "object",
            "properties": {
                "dn": {"type": "string", "description": "The DN of the SSH certificate"},
                "guid": {"type": "string", "description": "The GUID of the SSH certificate"}
            },
            "oneOf": [{"required": ["dn"]}, {"required": ["guid"]}]
        }
    )
)
async def retrieve_ssh_certificate(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    dn = arguments.get("dn")
    guid = arguments.get("guid")

    response = tpp.api.websdk.SSHCertificates.Retrieve.post(
        dn=dn,
        guid=guid
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]
