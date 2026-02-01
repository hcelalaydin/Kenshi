# Venafi MCP Server

An MCP server for Venafi Trust Protection Platform (TPP).

## Configuration

This server requires authentication to a Venafi TPP instance. You can configure it using environment variables:

- `VENAFI_URL`: The base URL of your Venafi TPP instance (e.g., `https://tpp.example.com/vedsdk`).
- `VENAFI_API_KEY`: Your API Key.
- `VENAFI_ACCESS_TOKEN`: Alternatively, use an Access Token.
- `VENAFI_USER` / `VENAFI_PASSWORD`: Alternatively, use username and password.

## Installation

```bash
pip install .
```

## Running

You can run the server using:

```bash
venafi-mcp-server
```

Or via `mcp` (if using fastmcp or similar runners, though this uses standard stdio server):

```bash
python -m venafi_mcp_server.server
```

## Available Tools

### Certificates
- `get_certificate_details`: Retrieve metadata for a certificate.
- `retrieve_certificate_data`: Download certificate content (Base64).
- `renew_certificate`: Renew a certificate.
- `revoke_certificate`: Revoke a certificate.
- `search_certificates`: Search for certificates.

### Config
- `list_objects`: Find configuration objects.
- `read_object`: Read object attributes.
- `write_object_attribute`: Write attributes to an object.
- `create_object`: Create a new object.
- `delete_object`: Delete an object.

### Identity
- `get_identity_self`: Get current user info.
- `browse_identities`: Search for users and groups.

### SSH Certificates
- `request_ssh_certificate`: Request an SSH certificate.
- `retrieve_ssh_certificate`: Retrieve an SSH certificate.

### Logs
- `query_logs`: Query TPP logs.
- `write_log`: Write a log entry.

## Dependencies

- `mcp`
- `pyvenafi`
