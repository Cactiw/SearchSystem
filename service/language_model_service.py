
from Resources import Resources


def count_probability(document: dict, request: dict, l: float) -> float:
    res = 1
    document_words = document.get("total_words", 0)
    if not document_words:
        return 0

    for word, word_count in request.get("words").items():
        r = (1 - l) * count_word_probability(word) + l * (document.get("words").get(word, 0) / document.get("total_words"))
        for i in range(word_count):
            res *= r
    return res


def count_word_probability(word: str) -> float:
    return Resources.words.get(word, {}).get("tf", 1) / Resources.total_words
