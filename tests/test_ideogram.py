from content_universe.catalog import Catalog
from content_universe.ideogram import extract_response_id_from_asset_url, generation_from_raw


def test_asset_response_id():
    url = "https://ideogram.ai/assets/image/balanced/response/abc123@2k"
    assert extract_response_id_from_asset_url(url) == "abc123"


def test_generation_ingest_and_merge():
    first = generation_from_raw(
        {
            "request_id": "req-1",
            "request_type": "TEXT_TO_IMAGE",
            "user_prompt": "hello",
            "responses": [{"response_id": "resp-1", "response_index": 0}],
        },
        "fixture:first",
    )
    richer = generation_from_raw(
        {
            "request_id": "req-1",
            "request_type": "TEXT_TO_IMAGE",
            "user_prompt": "hello",
            "seed": 42,
            "model_version": "V_4_0",
            "responses": [
                {
                    "response_id": "resp-1",
                    "response_index": 0,
                    "format": "PNG",
                    "num_likes": 3,
                }
            ],
        },
        "fixture:richer",
    )

    assert first is not None and richer is not None
    catalog = Catalog()
    catalog.ingest(first)
    catalog.ingest(richer)

    merged = catalog.generations["req-1"]
    assert merged.seed == 42
    assert merged.model_version == "V_4_0"
    assert merged.responses["resp-1"].format == "PNG"
    assert set(merged.sources) == {"fixture:first", "fixture:richer"}
