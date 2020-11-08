
import math

from Resources import Resources


def count_norm(vector: list) -> float:
    return sum(map(lambda x: x ** 2, vector)) ** 0.5


def normalize(vector: list) -> list:
    norm = count_norm(vector)
    if norm == 0:
        return vector
    return [(v / norm) for v in vector]


def count_document_vector(document: dict, words: dict, words_max: dict, N: int):
    vector = []
    for word, df in words.items():
        tf = document.get(word, 0)
        if Resources.USE_SECOND:
            second_value = 0.6 * (tf / words_max.get(word, 1))
            tf = (0.4 + second_value) if second_value else 0

        value = tf * df.get("idf")  # tf * log (N / df)
        vector.append(value)
    vector = normalize(vector)
    return vector


def cosine(v1: list, v2: list) -> float:
    norm_1, norm_2 = count_norm(v1), count_norm(v2)
    if norm_1 == 0 or norm_2 == 0:
        return 0
    result = sum([val1 * val2 for val1, val2 in zip(v1, v2)]) / (norm_1 * norm_2)
    if result > 0.9:
        print(result)
    return sum([val1 * val2 for val1, val2 in zip(v1, v2)]) / (norm_1 * norm_2)
