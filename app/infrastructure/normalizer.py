import pymorphy2

class MorphNormalizer:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def normalize(self, word: str) -> str:
        return self.morph.parse(word)[0].normal_form