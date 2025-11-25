from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).with_name("tokens.yaml")


class TokenNotFound(Exception):
    """Raised when a requested token/network combination is not found in the registry."""
    pass


@lru_cache(maxsize=1)
def _load_tokens() -> dict[tuple[str, str], dict]:
    """
    Load tokens from the YAML configuration file and index them by (symbol, network).
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or []

    index: dict[tuple[str, str], dict] = {}
    for t in raw:
        symbol = str(t["symbol"]).upper()
        network = str(t["network"]).lower()
        key = (symbol, network)
        index[key] = t
    return index


def get_token(symbol: str, network: str) -> dict:
    """
    Return the token metadata dict for a given symbol and network.

    :param symbol: Token symbol, e.g. "USDT"
    :param network: Network identifier, e.g. "tron", "ethereum", "bitcoin"
    :raises TokenNotFound: if the combination is not present in the registry.
    """
    symbol = symbol.upper()
    network = network.lower()
    tokens = _load_tokens()
    key = (symbol, network)

    if key not in tokens:
        raise TokenNotFound(f"{symbol} on {network} not found")
    return tokens[key]


def list_tokens(network: str | None = None) -> list[dict]:
    """
    List all tokens, optionally filtered by network.

    :param network: If provided, only tokens on this network are returned.
    """
    tokens = _load_tokens()
    if network:
        network = network.lower()
        return [t for (sym, net), t in tokens.items() if net == network]
    return list(tokens.values())
