
import pymorphy2
import string
import re
import os
import glob
import math
import unicodedata
import json

import tqdm

from Resources import Resources


from service.dict_service import increase_or_add_value_to_dict, merge_int_dictionaries, save_dict
from service.vector_service import normalize, count_document_vector, count_norm, cosine
from service.language_model_service import count_probability


def analyse_text(text_in, max_words) -> (dict, dict):
    text = re.sub("\\[.+?\\]", "", text_in)
    text = remove_accents(text)
    morph = pymorphy2.MorphAnalyzer()

    result, total_words = {}, {}

    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    for sentence in tqdm.tqdm(sentences):
        count_words = 0
        sent_words = {}
        normalized_words = list(map(lambda word: normal_form(morph, word.strip()), re.sub("[—{}\\n«»]".format("".join(string.punctuation)), " ", sentence).split()))
        normalized_sentence = " ".join(normalized_words)
        words = set(normalized_words)
        for word in words:
            max_word = max_words.get(word, 0)

            tf = 0
            for cur_word in normalized_sentence.split():
                if word == cur_word:
                    tf += 1
                    count_words += 1

            # tf = normalized_sentence.count(word)
            increase_or_add_value_to_dict(sent_words, word, tf)
            increase_or_add_value_to_dict(total_words, word, 1)
            if tf > max_word:
                max_words.update({word: tf})

        if count_words > 0:
            result.update({sentence.replace("\n", ""): {
                "words": sent_words,
                "total_words": count_words
            }})
    return result, total_words


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normal_form(morph, word) -> str:
    return morph.parse(word)[0].normal_form


def parse_input() -> (dict, dict, dict, dict):
    try:
        f = open("documents.json", encoding="utf-8", mode='r')
        documents = json.load(f)
        f.close()

        f = open("words.json", encoding="utf-8", mode='r')
        words = json.load(f)
        f.close()

        f = open("vectors.json", encoding="utf-8", mode='r')
        vectors = json.load(f)
        f.close()

        f = open("max_words.json", encoding="utf-8", mode='r')
        max_words = json.load(f)
        f.close()

        total_words = count_total_words(words)

        print("Cache files exist!")
        return documents, words, vectors, max_words, total_words

    except FileNotFoundError:
        pass

    print("Cache not found, generating now! (First launch)")

    documents = {}
    words = {}
    max_words = {}

    for filename in glob.glob('input/*.txt'):
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as f:
            name = filename.partition("input\\")[2]
            print("Parsing {}".format(name))
            res, cur_words = analyse_text(f.read(), max_words)
            documents.update(res)
            merge_int_dictionaries(words, cur_words)

    print("Processed {} documents with {} words".format(len(documents), len(words)))
    print("Calculating vectors...", flush=True)
    words = {k: {"tf": v, "idf": (1 / v if not Resources.USE_SECOND else math.log(len(documents) / v))} for k, v in words.items()}
    vectors = {}
    for document, d_words in tqdm.tqdm(documents.items()):
        vector = count_document_vector(d_words["words"], words, max_words, len(documents))
        vectors.update({document: vector})

    save_dict(documents, "documents.json")
    save_dict(words, "words.json")
    save_dict(vectors, "vectors.json")
    save_dict(max_words, "max_words.json")

    total_words = count_total_words(words)
    return documents, words, vectors, max_words, total_words

    # tf - вхождения слова в ЭТОТ документ
    # N - количество документов всего
    # df - количество документов, в которое это слово входит хотя бы один раз

    # log2 (1 + tf) * log10 (N / df) - неверно
    # tf * log (N / df)


def count_total_words(words: dict) -> int:
    total_words = 0
    for word_dict in words.values():
        total_words += word_dict.get("tf", 0)
    return total_words


def perform_query(request: str) -> list:
    documents, words, vectors, max_words = Resources.get_resources()
    res, cur_words = analyse_text(request, max_words)
    result = []

    if Resources.USE_VECTOR:
        # Векторная модель
        request_vector = count_document_vector(list(res.values())[0]["words"], words, max_words, len(documents))
        for name, vector in vectors.items():
            result.append([name, cosine(vector, request_vector)])
    else:
        # Языковая модель
        for doc_name, doc_data in documents.items():
            result.append([doc_name, count_probability(doc_data, list(res.values())[0], Resources.LAMBDA)])

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def count_dcg(l: list) -> float:
    res = 0
    print("Counting DCG of {}:".format(l))
    for i, elem in enumerate(l):
        res += elem / math.log(i + 1 + 1, 2)
        print("+ {} / log2({})".format(elem, i + 1 + 1), end=" ")
    print("\nDCG = {}".format(res))
    return res


# i_dcg = count_dcg([2, 1, 1, 0, 0, 0, 0, 0, 0, 0])
# print(i_dcg)
#
# print(count_dcg([2, 1, 1, 0, 0, 0, 0, 0, 0, 0]) / i_dcg)
# print(count_dcg([2, 0, 0, 1, 0, 0, 0, 0, 0, 0]) / i_dcg)
# print(count_dcg([1, 1, 2, 1, 0, 1, 1, 0, 1, 0]) / i_dcg)
# print(count_dcg([1, 1, 2, 1, 0, 1, 1, 0, 0, 0]) / i_dcg)
