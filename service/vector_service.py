
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
        value = math.log(document["words"].get(word, 0) + 1, 2) * math.log(N / df, 10)
        vector.append(value)
    vector = normalize(vector)
    return vector
