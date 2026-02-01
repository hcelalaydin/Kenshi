import json
import mcp.types as types
from venafi_mcp_server.registry import registry
from venafi_mcp_server.client import get_tpp_client
from pyvenafi.tpp.api.websdk.models import certificate

@registry.register(
    types.Tool(
        name="get_certificate_details",
        description="Retrieve certificate metadata and details by DN or GUID.",
        inputSchema={
            "type": "object",
            "properties": {
                "certificate_dn": {"type": "string", "description": "The DN of the certificate"},
                "guid": {"type": "string", "description": "The GUID of the certificate"}
            },
            "oneOf": [{"required": ["certificate_dn"]}, {"required": ["guid"]}]
        }
    )
)
async def get_certificate_details(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    cert_dn = arguments.get("certificate_dn")
    guid = arguments.get("guid")

    if cert_dn and not guid:
        # Resolve DN to GUID
        resp = tpp.api.websdk.Config.DnToGuid.post(object_dn=cert_dn)
        if resp.result.code != 1:
            return [types.TextContent(type="text", text=f"Error resolving DN to GUID: {resp.result}")]
        guid = resp.guid

    response = tpp.api.websdk.Certificates.Guid(guid).get()

    # Serialize response to JSON
    # pyvenafi models usually have .dict() or are pydantic models
    if hasattr(response, 'dict'):
        data = response.dict(by_alias=True, exclude_none=True)
    elif hasattr(response, 'api_response'):
        data = response.api_response
    else:
        data = str(response)

    return [types.TextContent(type="text", text=json.dumps(data, indent=2, default=str))]

@registry.register(
    types.Tool(
        name="retrieve_certificate_data",
        description="Download the actual certificate data (Base64) by DN.",
        inputSchema={
            "type": "object",
            "properties": {
                "certificate_dn": {"type": "string", "description": "The DN of the certificate"},
                "format": {"type": "string", "enum": ["Base64", "DER", "PKCS7", "PKCS12", "JKS"], "default": "Base64"},
                "include_private_key": {"type": "boolean", "default": False},
                "password": {"type": "string", "description": "Password for PKCS12/JKS/PrivateKey"}
            },
            "required": ["certificate_dn"]
        }
    )
)
async def retrieve_certificate_data(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    cert_dn = arguments.get("certificate_dn")
    fmt = arguments.get("format", "Base64")
    include_private_key = arguments.get("include_private_key", False)
    password = arguments.get("password")

    # Map format string to Enum if necessary, usually pyvenafi handles string if it matches enum values
    # The Enum is certificate.CertificateFormat

    response = tpp.api.websdk.Certificates.Retrieve.post(
        certificate_dn=cert_dn,
        format=fmt,
        friendly_name="mcp_retrieve", # Required param
        include_private_key=include_private_key,
        password=password
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="renew_certificate",
        description="Renew a certificate.",
        inputSchema={
            "type": "object",
            "properties": {
                "certificate_dn": {"type": "string", "description": "The DN of the certificate to renew"}
            },
            "required": ["certificate_dn"]
        }
    )
)
async def renew_certificate(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    cert_dn = arguments.get("certificate_dn")

    response = tpp.api.websdk.Certificates.Renew.post(certificate_dn=cert_dn)

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="revoke_certificate",
        description="Revoke a certificate.",
        inputSchema={
            "type": "object",
            "properties": {
                "certificate_dn": {"type": "string", "description": "The DN of the certificate to revoke"},
                "reason": {"type": "integer", "description": "Revocation reason code (0=Unspecified, 1=KeyCompromise, etc.)", "default": 0},
                "comments": {"type": "string", "description": "Comments for revocation"}
            },
            "required": ["certificate_dn"]
        }
    )
)
async def revoke_certificate(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    cert_dn = arguments.get("certificate_dn")
    reason = arguments.get("reason", 0)
    comments = arguments.get("comments")

    response = tpp.api.websdk.Certificates.Revoke.post(
        certificate_dn=cert_dn,
        reason=reason,
        comments=comments
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]

@registry.register(
    types.Tool(
        name="search_certificates",
        description="Search for certificates.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 100},
                "offset": {"type": "integer", "default": 0},
                "dn_pattern": {"type": "string", "description": "Filter by DN pattern"}
            }
        }
    )
)
async def search_certificates(arguments: dict) -> list[types.TextContent]:
    tpp = get_tpp_client()
    limit = arguments.get("limit")
    offset = arguments.get("offset")
    dn_pattern = arguments.get("dn_pattern")

    # Note: Search filters in pyvenafi are usually a dictionary or object
    # The 'filters' argument in get() accepts a dictionary.
    filters = {}
    if dn_pattern:
        filters['ConfigDN'] = dn_pattern # Usually standard TPP filter

    response = tpp.api.websdk.Certificates.get(
        limit=limit,
        offset=offset,
        filters=filters
    )

    return [types.TextContent(type="text", text=json.dumps(response.dict(by_alias=True), indent=2))]
