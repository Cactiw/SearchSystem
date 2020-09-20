
import pymorphy2
import string
import json
import re
import multiprocessing

import tqdm

from dict_service import increase_or_add_value_to_dict

PROCESS_NUM = 4


def analyse_text(file) -> dict:
    text_words = re.sub("[—{}]".format("".join(string.punctuation)), " ", file.read()).split()
    morph = pymorphy2.MorphAnalyzer()
    result = {}

    with multiprocessing.Pool(PROCESS_NUM) as pool:
        for normal_form in tqdm.tqdm(pool.imap_unordered(analyse_word, [(morph, word) for word in text_words]),
                                     total=len(text_words)):
            increase_or_add_value_to_dict(result, normal_form, 1)
    return result


def analyse_word(in_obj: list):
    morph, word = in_obj
    return morph.parse(word)[0].normal_form


def main():
    f = open("input.txt", encoding="utf-8")
    result = {k: v for k, v in sorted(analyse_text(f).items(), key=lambda elem: elem[1], reverse=True)}
    f.close()

    out = open("output.json", encoding="utf-8", mode="w")
    out.write(json.dumps(result, indent=4, ensure_ascii=False))
    out.close()


if __name__ == "__main__":
    main()
