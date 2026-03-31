import os
import json
import requests
from typing import List, Dict, Any
from langchain_core.tools import tool
from newsapi import NewsApiClient
import streamlit as st

FREECRYPTO_TOKEN = st.secrets.get("FREECRYPTO_TOKEN") or os.getenv('FREECRYPTO_TOKEN')
NEWSAPI_KEY = st.secrets.get("NEWSAPI_KEY") or os.getenv('NEWSAPI_KEY')


@tool
def crypto_list_tool(limit: int = 25) -> str:
    """
    Fetches a list of available cryptocurrencies (symbol + name) from FreeCryptoAPI.
    Args:
        limit (int): Max number of coins to return (to keep responses compact).
    Returns:
        str: JSON string with a condensed list: [{"symbol": "...", "name": "..."}, ...]
    """
    url = "https://api.freecryptoapi.com/v1/getCryptoList"
    headers = {"Authorization": f"Bearer {FREECRYPTO_TOKEN}"}
    resp = requests.get(url, headers=headers, timeout=30)

    try:
        data = resp.json()
    except Exception:
        return json.dumps({"status": False, "error": "Invalid JSON from API"})

    if isinstance(data, list):
        slim = []
        for item in data[: max(1, limit)]:
            sym = item.get("symbol") or item.get("Symbol") or item.get("ticker")
            nm = item.get("name") or item.get("Name")
            if sym or nm:
                slim.append({"symbol": sym, "name": nm})
        return json.dumps({"status": True, "coins": slim}, indent=2)

    return json.dumps(data, indent=2)


@tool
def crypto_data_tool(symbol: str) -> str:
    """
    Fetches detailed data for a given crypto symbol (e.g., BTC) from FreeCryptoAPI.
    Args:
        symbol (str): Ticker symbol like 'BTC', 'ETH', etc.
    Returns:
        str: JSON string of the API response.
    """
    url = "https://api.freecryptoapi.com/v1/getData"
    headers = {"Authorization": f"Bearer {FREECRYPTO_TOKEN}"}
    params = {"symbol": symbol.upper().strip()}
    resp = requests.get(url, headers=headers, params=params, timeout=30)

    try:
        data = resp.json()
    except Exception:
        return json.dumps({"status": False, "error": "Invalid JSON from API"})

    return json.dumps(data, indent=2)


@tool
def crypto_news_tool(query: str = "crypto", mode: str = "top", max_items: int = 5) -> str:
    """
    Fetches recent/important news using NewsAPI and returns a condensed list.
    Args:
        query (str): Search query, e.g. 'bitcoin', 'ethereum', 'crypto regulation'
        mode (str): unused, kept for compatibility
        max_items (int): Max number of articles to return. (default: 5)
    Returns:
        str: JSON string with fields: title, source, url, publishedAt
    """
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    try:
        res = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page=1,
        )
        articles = res.get("articles", [])
    except Exception as e:
        return json.dumps({"status": False, "error": str(e)})

    slim: List[Dict[str, Any]] = []
    for a in articles[: max(1, max_items)]:
        slim.append(
            {
                "title": a.get("title"),
                "source": (a.get("source") or {}).get("name"),
                "url": a.get("url"),
                "publishedAt": a.get("publishedAt"),
            }
        )

    return json.dumps(
        {
            "status": True,
            "totalResults": len(articles),
            "returned": len(slim),
            "articles": slim,
        },
        indent=2,
    )


ALL_TOOLS = [crypto_list_tool, crypto_data_tool, crypto_news_tool]
