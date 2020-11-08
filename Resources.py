

class Resources:
    documents, words, vectors, max_words = {}, {}, {}, {}
    total_words = 0
    requests = [
        "Платоническая возлюбленная Огюста Конта вдохновила его на создание «религии человечества»",
        "Рыбак, ударивший веслом по голове короля Гавайев, не был наказан, поскольку всего лишь защищался",
        "Одна из мечетей в Крыму построена в честь неудачного покушения на императора"
    ]
    USE_SECOND = False
    USE_VECTOR = False
    LAMBDA = 0.5

    @classmethod
    def set_resources(cls, documents: dict, words: dict, vectors: dict, max_words: dict, total_words: int):
        cls.documents = documents
        cls.words = words
        cls.vectors = vectors
        cls.max_words = max_words
        cls.total_words = total_words

    @classmethod
    def get_resources(cls) -> (dict, dict, dict):
        return cls.documents, cls.words, cls.vectors, cls.max_words
