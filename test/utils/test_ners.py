from osint.utils.ners import html_ner


def test_html_ner():
    test = 'Hello, my name is Sinderella'
    result = html_ner(test)
    expected = [(u'PERSON', 'Sinderella')]
    assert result == expected
