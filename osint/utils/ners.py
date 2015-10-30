from itertools import groupby

from bs4 import BeautifulSoup
from nltk import StanfordNERTagger, wordpunct_tokenize


def url_ner(content):
    st = StanfordNERTagger(
        './lib/classifiers/english.all.3class.distsim.crf.ser.gz',
        './lib/stanford-ner.jar')
    soup = BeautifulSoup(content, "html.parser")
    for script in soup(["script", "style", "sup"]):
        script.extract()
    tokenised_sents = list(soup.stripped_strings)
    tokenised_words = [wordpunct_tokenize(sent) for sent in tokenised_sents]
    tagged_sents = [st.tag(sent) for sent in tokenised_words]

    result = list()

    for sent in tagged_sents:
        for tag, chunk in groupby(sent, lambda x: x[1]):
            if tag != 'O':
                result.append((tag, ' '.join(w for w, t in chunk).encode('utf-8').strip()))
    return result
