import json

from content_universe.adapters.ideogram.models import filter_models, model_records
from content_universe.network import endpoint_inventory
from content_universe.sanitize import sanitize_har


def test_model_capabilities_fixture():
    payload = {
        "models": [{
            "model_id": "m1",
            "supports_style_reference": True,
            "supports_product_reference": False,
            "is_custom_model": False,
            "available_resolution_tiers": ["1K", "2K"],
        }]
    }
    records = model_records(payload)
    assert len(records) == 1
    assert records[0].capabilities["supports_style_reference"] is True
    assert filter_models(records, capability="supports_style_reference") == records
    assert filter_models(records, custom=True) == []


def test_sanitizer_redacts_headers_and_query():
    har = {
        "log": {"entries": [{
            "request": {
                "url": "https://example.test/api?token=secret",
                "headers": [{"name": "Authorization", "value": "Bearer secret"}],
                "queryString": [{"name": "token", "value": "secret"}],
            },
            "response": {
                "status": 200,
                "headers": [{"name": "Set-Cookie", "value": "session=secret"}],
                "content": {"mimeType": "application/json", "text": "{\"ok\":true}"},
            },
        }]}
    }
    clean = sanitize_har(har)
    entry = clean["log"]["entries"][0]
    assert entry["request"]["headers"][0]["value"] == "<REDACTED>"
    assert entry["request"]["queryString"][0]["value"] == "<REDACTED>"
    assert entry["response"]["headers"][0]["value"] == "<REDACTED>"


def test_network_inventory(tmp_path):
    har = {
        "log": {"entries": [{
            "request": {"method": "GET", "url": "https://ideogram.ai/api/example?cursor=secret"},
            "response": {"status": 200, "content": {"mimeType": "application/json"}},
        }]}
    }
    path = tmp_path / "ideogram.har"
    path.write_text(json.dumps(har))
    items = endpoint_inventory(path, host="ideogram.ai")
    assert items[0].path == "/api/example"
    assert "cursor=" not in items[0].sample_urls[0]
