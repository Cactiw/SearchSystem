
import pymorphy2
import string
import re
import os
import glob
import math
import unicodedata

import tqdm

from service.dict_service import increase_or_add_value_to_dict, merge_int_dictionaries, save_dict
from service.vector_service import normalize

PROCESS_NUM = 4


def analyse_text(file) -> (dict, dict):
    text = file.read()
    text = re.sub("\\[.+?\\]", "", text)
    text = remove_accents(text)
    morph = pymorphy2.MorphAnalyzer()

    result, total_words = {}, {}

    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    for sentence in tqdm.tqdm(sentences):
        sent_words = {}
        normalized_words = list(map(lambda word: normal_form(morph, word.strip()), re.sub("[—{}\\n]".format("".join(string.punctuation)), " ", sentence).split()))
        normalized_sentence = " ".join(normalized_words)
        words = set(normalized_words)
        for word in words:
            increase_or_add_value_to_dict(sent_words, word, normalized_sentence.count(word))
            increase_or_add_value_to_dict(total_words, word, 1)
        result.update({sentence: {
            "words": sent_words
        }})
    return result, total_words


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normal_form(morph, word) -> str:
    return morph.parse(word)[0].normal_form


def parse_input() -> dict:
    documents = {}
    words = {}

    for filename in glob.glob('input/*.txt'):
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as f:
            name = filename.partition("input\\")[2]
            print("Parsing {}".format(name))
            res, cur_words = analyse_text(f)
            documents.update(res)
            merge_int_dictionaries(words, cur_words)

    print("Processed {} documents with {} words".format(len(documents), len(words)))
    print("Calculating vectors...", flush=True)
    vectors = {}
    for document, d_words in tqdm.tqdm(documents.items()):
        vector = []
        for word, df in words.items():
            value = math.log(d_words["words"].get(word, 0) + 1, 2) * math.log(len(documents) / df, 10)
            vector.append(value)
        vector = normalize(vector)
        vectors.update({document: vector})

    save_dict(documents, "documents.json")
    save_dict(words, "words.json")
    save_dict(vectors, "vectors.json")

    return vectors

    # tf - вхождения слова в ЭТОТ документ
    # N - количество документов всего
    # df - количество документов, в которое это слово входит хотя бы один раз

    # log2 (1 + tf) * log10 (N / df)


def main():
    parse_input()


if __name__ == "__main__":
    main()
