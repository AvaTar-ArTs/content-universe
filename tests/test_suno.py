from content_universe.adapters.suno.csv import SunoCsvAdapter
from content_universe.adapters.suno.html import SunoHtmlAdapter


def test_suno_csv_adapter(tmp_path):
    path = tmp_path / "suno.csv"
    path.write_text(
        "id,title,audioUrl,lyrics\n"
        "123e4567-e89b-12d3-a456-426614174000,Song,https://cdn.example.invalid/123e4567-e89b-12d3-a456-426614174000.mp3,hello\n"
    )
    adapter = SunoCsvAdapter()
    assert adapter.supports(path)
    result = adapter.harvest(path)
    assert len(result.records) == 1
    record = result.records[0]
    assert record.request_id == "suno:123e4567-e89b-12d3-a456-426614174000"
    assert record.responses["123e4567-e89b-12d3-a456-426614174000"].raw["lyrics"] == "hello"


def test_suno_html_next_data_adapter(tmp_path):
    path = tmp_path / "suno.html"
    path.write_text('''<!doctype html><html><head><title>Suno</title></head><body>
    <script id="__NEXT_DATA__" type="application/json">{
      "props":{"clips":[{
        "id":"123e4567-e89b-12d3-a456-426614174001",
        "title":"HTML Song",
        "audio_url":"https://cdn.example.invalid/123e4567-e89b-12d3-a456-426614174001.mp3",
        "metadata":{"lyrics":"hello html","prompt":"test"}
      }]}
    }</script></body></html>''')
    adapter = SunoHtmlAdapter()
    assert adapter.supports(path)
    result = adapter.harvest(path)
    assert len(result.records) == 1
    record = result.records[0]
    response = record.responses["123e4567-e89b-12d3-a456-426614174001"]
    assert response.raw["lyrics"] == "hello html"
    assert response.prompt == "test"
