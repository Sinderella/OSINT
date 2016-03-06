from osint.plugins.google import Google


def test_query_sanity():
    query = "test"
    google = Google
    google.query = query
    assert google.query == query