

def count_norm(vector: list) -> float:
    return sum(map(lambda x: x ** 2, vector)) ** 0.5


def normalize(vector: list) -> list:
    norm = count_norm(vector)
    if norm == 0:
        return vector
    return [(v / norm) for v in vector]
