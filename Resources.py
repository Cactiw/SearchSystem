

class Resources:
    documents, words, vectors = {}, {}, {}
    requests = [
        "Платоническая возлюбленная Огюста Конта вдохновила его на создание «религии человечества»",
        "Рыбак, ударивший веслом по голове короля Гавайев, не был наказан, поскольку всего лишь защищался",
        "Одна из мечетей в Крыму построена в честь неудачного покушения на императора"
    ]

    @classmethod
    def set_resources(cls, documents: dict, words: dict, vectors: dict):
        cls.documents = documents
        cls.words = words
        cls.vectors = vectors

    @classmethod
    def get_resources(cls) -> (dict, dict, dict):
        return cls.documents, cls.words, cls.vectors
