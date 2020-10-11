

def count_norm(vector: list) -> float:
    return sum(map(lambda x: x ** 2, vector)) ** 0.5


def normalize(vector: list) -> list:
    norm = count_norm(vector)
    return [(v / norm) for v in vector]
