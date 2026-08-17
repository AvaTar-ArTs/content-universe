import json

from content_universe.adapters.ideogram.html import IdeogramHtmlAdapter
from content_universe.promptlab import decompose_prompt, prompt_fingerprint


def test_html_adapter_extracts_generation_and_response(tmp_path):
    html = '''<html><head><title>Ideogram</title></head><body>
    <div data-testid="image-grid-item-GEN123"><a href="/g/GEN123/2">
    <img src="https://ideogram.ai/assets/image/balanced/response/RESP456@2k"></a></div>
    </body></html>'''
    path = tmp_path / "ideogram-page.html"
    path.write_text(html)
    result = IdeogramHtmlAdapter().harvest(path)
    assert len(result.records) == 1
    record = result.records[0]
    assert record.request_id == "GEN123"
    assert "RESP456" in record.responses
    assert record.responses["RESP456"].response_index == 2
    assert len(result.graph.edges) == 1


def test_prompt_decomposition_handles_ideogram_structured_prompt():
    expanded = json.dumps({
        "high_level_description": "A poster",
        "compositional_deconstruction": {
            "background": "black",
            "elements": [
                {"type": "obj", "desc": "large moon"},
                {"type": "text", "text": "HELLO", "desc": "bold headline"},
            ],
        },
    })
    decomposition = decompose_prompt("poster please", expanded)
    assert decomposition.is_structured
    assert decomposition.high_level_description == "A poster"
    assert decomposition.background == "black"
    assert len(decomposition.elements) == 2
    fingerprint = prompt_fingerprint(decomposition)
    assert fingerprint["text_elements"] == 1
    assert fingerprint["element_kinds"] == {"obj": 1, "text": 1}
