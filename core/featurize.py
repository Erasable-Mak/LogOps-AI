from sklearn.feature_extraction.text import HashingVectorizer

class TextFeaturizer:
    def __init__(self):
        self._vect = HashingVectorizer(n_features=2**18, alternate_sign=False, norm="l2", analyzer="word", ngram_range=(1,2))

    def transform(self, texts: list[str]):
        return self._vect.transform(texts)
