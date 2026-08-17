import json

from content_universe.adapters.ideogram.browser_export import IdeogramBrowserExportAdapter


def test_browser_export_adapter(tmp_path):
    path = tmp_path / "content-universe-ideogram.json"
    path.write_text(json.dumps([
        {
            "platform": "ideogram",
            "generation_id": "GEN001",
            "response_id": "RESP001",
            "response_index": 3,
            "generation_url": "https://ideogram.ai/g/GEN001/3",
            "asset_url": "https://ideogram.ai/assets/image/balanced/response/RESP001@2k",
            "asset_resolution": "2k",
            "feed": "explore",
            "observed_at": "2026-08-17T00:00:00+00:00",
            "source": "ideogram-userscript-dom"
        }
    ]))
    adapter = IdeogramBrowserExportAdapter()
    assert adapter.supports(path)
    result = adapter.harvest(path)
    assert len(result.records) == 1
    response = result.records[0].responses["RESP001"]
    assert response.response_index == 3
    assert response.asset_url.endswith("RESP001@2k")
    assert len(result.graph.edges) == 1
