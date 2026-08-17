from content_universe.adapters.ideogram.profile import build_profile_url, walk_profile


def test_build_profile_url_contains_cursor():
    url = build_profile_url("avatararts", cursor="abc 123")
    assert "display_handle=avatararts" in url
    assert "cursor=abc+123" in url


def test_walk_profile_stops_and_normalizes():
    pages = {
        0: {"results": [{"request_id": "r1", "responses": [{"response_id": "a", "response_index": 0}]}], "next_cursor": "next"},
        1: {"results": [{"request_id": "r2", "responses": [{"response_id": "b", "response_index": 0}]}]},
    }
    calls = []

    def transport(url):
        calls.append(url)
        return pages[0] if len(calls) == 1 else pages[1]

    result = list(walk_profile("avatararts", transport))
    assert len(result) == 2
    assert [page.records[0].request_id for page in result] == ["r1", "r2"]
