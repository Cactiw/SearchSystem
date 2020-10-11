
import math


def count_norm(vector: list) -> float:
    return sum(map(lambda x: x ** 2, vector)) ** 0.5


def normalize(vector: list) -> list:
    norm = count_norm(vector)
    if norm == 0:
        return vector
    return [(v / norm) for v in vector]


def count_document_vector(document: dict, words: dict, N: int):
    vector = []
    for word, df in words.items():
        value = math.log(document.get(word, 0) + 1, 2) * math.log(N / df, 10)
        vector.append(value)
    vector = normalize(vector)
    return vector


def cosine(v1: list, v2: list) -> float:
    norm_1, norm_2 = count_norm(v1), count_norm(v2)
    if norm_1 == 0 or norm_2 == 0:
        return 0
    return sum([val1 * val2 for val1, val2 in zip(v1, v2)]) / (norm_1 * norm_2)
