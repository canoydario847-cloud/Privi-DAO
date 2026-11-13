#!/usr/bin/env python3
"""Privi AI DAO: read-only service inspection and maintenance proposal generation.

No autonomous deployments, wallet signing, payments, or repository mutations.
Python 3.11+, standard library only.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import socket
import urllib.error
import urllib.parse
import urllib.request

UTC = dt.timezone.utc
ALLOWED_SCHEMES = {"https"}  # explicitly deny local/file/http endpoints


def utc_now():
    return dt.datetime.now(UTC).isoformat()


def validate_target(target):
    name, url = target.get("name"), target.get("url")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("target name required")
    if not isinstance(url, str):
        raise ValueError(f"{name}: URL required")
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError(f"{name}: publicly reachable HTTPS URL required")
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError(f"{name}: URL credentials/fragments prohibited")
    return name, url


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def inspect(target, timeout=8):
    name, url = validate_target(target)
    # Reject DNS resolution to local/private address ranges to avoid SSRF.
    import ipaddress
    hostname = urllib.parse.urlsplit(url).hostname
    try:
        addresses = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
        for a in addresses:
            ip = ipaddress.ip_address(a[4][0])
            if not ip.is_global:
                raise ValueError(f"{name}: non-public address prohibited")
    except socket.gaierror as exc:
        return {"name": name, "url": url, "state": "unknown", "error": "dns_failed"}
    req = urllib.request.Request(url, headers={"User-Agent": "PriviDAO-Monitor/0.1"}, method="GET")
    try:
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(req, timeout=timeout) as response:
            code = response.status
        state = "healthy" if 200 <= code < 400 else "degraded"
        return {"name": name, "url": url, "state": state, "status_code": code}
    except urllib.error.HTTPError as exc:
        return {"name": name, "url": url, "state": "degraded" if exc.code < 500 else "unhealthy", "status_code": exc.code}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"name": name, "url": url, "state": "unknown", "error": type(exc).__name__}


def proposals_for(results, run_id):
    proposals = []
    for r in results:
        if r["state"] == "healthy":
            continue
        action = "Investigate service health and verify logs, DNS, TLS, and deployment status"
        proposals.append({
            "id": hashlib.sha256((run_id + "|" + r["name"]).encode()).hexdigest()[:16],
            "type": "maintenance",
            "target": r["name"],
            "finding": r["state"],
            "recommended_action": action,
            "risk": "low",
            "status": "proposed",
            "execution": "blocked_until_human_approval",
            "evidence": {"url": r["url"], "status_code": r.get("status_code"), "error": r.get("error")},
        })
    return proposals


def run(config):
    targets = config.get("targets", [])
    if not isinstance(targets, list):
        raise ValueError("targets must be a list")
    names = set()
    for t in targets:
        name, _ = validate_target(t)
        if name in names:
            raise ValueError(f"duplicate target: {name}")
        names.add(name)
    timestamp = utc_now()
    results = [inspect(t) for t in targets]
    digest = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
    run_id = timestamp + "-" + digest
    return {
        "schema_version": "1",
        "operator": "privi-ai-dao",
        "run_id": run_id,
        "generated_at": timestamp,
        "mode": "read_only",
        "service_results": results,
        "proposals": proposals_for(results, run_id),
        "governance": {
            "human_approval_required_for": [
                "deployments", "merges", "security_changes", "treasury_transfers",
                "token_minting", "mainnet_changes", "production_remediation"
            ],
            "autonomous_treasury_access": False,
            "automatic_execution": False
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="dao/targets.json")
    parser.add_argument("--output", default="reports/latest.json")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    report = run(config)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Inspected {len(report['service_results'])} targets; proposed {len(report['proposals'])} investigations. Report: {output}")


if __name__ == "__main__":
    main()
