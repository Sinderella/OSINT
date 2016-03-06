from osint.plugins.bing import Bing


def test_query_sanity():
    query = "test"
    bing = Bing
    bing.query = query
    assert bing.query == query
