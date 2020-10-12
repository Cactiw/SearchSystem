

class Resources:
    documents, words, vectors, max_words = {}, {}, {}, {}
    requests = [
        "Платоническая возлюбленная Огюста Конта вдохновила его на создание «религии человечества»",
        "Рыбак, ударивший веслом по голове короля Гавайев, не был наказан, поскольку всего лишь защищался",
        "Одна из мечетей в Крыму построена в честь неудачного покушения на императора"
    ]
    USE_SECOND = True

    @classmethod
    def set_resources(cls, documents: dict, words: dict, vectors: dict, max_words: dict):
        cls.documents = documents
        cls.words = words
        cls.vectors = vectors
        cls.max_words = max_words

    @classmethod
    def get_resources(cls) -> (dict, dict, dict):
        return cls.documents, cls.words, cls.vectors, cls.max_words
