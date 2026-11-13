#!/usr/bin/env python3
"""Validate the Privi DAO off-chain service catalog (standard library only)."""
import json
from pathlib import Path
from urllib.parse import urlsplit

def validate(catalog):
    items = catalog["services"]
    ids = set()
    for item in items:
        assert item["id"] and item["id"] not in ids, "duplicate/empty id"
        ids.add(item["id"])
        assert item["name"] and item["type"] in {"repository", "website", "api", "project"}
        assert item["governance"] == "catalog_only", "catalog cannot claim on-chain control"
        if item["url"]:
            p = urlsplit(item["url"])
            assert p.scheme == "https" and p.hostname, "invalid URL"
    return len(items)

if __name__ == "__main__":
    print("Validated", validate(json.loads(Path("services/catalog.json").read_text())), "services")
