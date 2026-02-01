import os
from pyvenafi.tpp import TPP

_tpp_client = None

def get_tpp_client() -> TPP:
    global _tpp_client
    if _tpp_client:
        return _tpp_client

    url = os.environ.get("VENAFI_URL")
    api_key = os.environ.get("VENAFI_API_KEY")
    access_token = os.environ.get("VENAFI_ACCESS_TOKEN")
    user = os.environ.get("VENAFI_USER")
    password = os.environ.get("VENAFI_PASSWORD")

    if not url:
        raise ValueError("VENAFI_URL environment variable is required")

    # Auth priority: API Key > Access Token > User/Pass
    if api_key:
        _tpp_client = TPP(url=url, api_key=api_key)
    elif access_token:
        _tpp_client = TPP(url=url, access_token=access_token)
    elif user and password:
        _tpp_client = TPP(url=url, user=user, password=password)
    else:
        raise ValueError("Venafi credentials required (VENAFI_API_KEY, VENAFI_ACCESS_TOKEN, or VENAFI_USER/VENAFI_PASSWORD)")

    return _tpp_client
