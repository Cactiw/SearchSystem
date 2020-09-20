
import pymorphy2
import string
import json
import re

import tqdm

from dict_service import increase_or_add_value_to_dict

PROCESS_NUM = 4


def analyse_text(file) -> dict:
    text = re.sub("[—{}]".format("".join(string.punctuation)), " ", file.read())
    morph = pymorphy2.MorphAnalyzer()

    result = {}

    for word in tqdm.tqdm(text.split()):
        word = word.strip()
        parsed = morph.parse(word)[0].normal_form
        increase_or_add_value_to_dict(result, parsed, 1)
    return result


def main():
    f = open("input.txt", encoding="utf-8")
    result = {k: v for k, v in sorted(analyse_text(f).items(), key=lambda elem: elem[1], reverse=True)}
    f.close()

    out = open("output.json", encoding="utf-8", mode="w")
    out.write(json.dumps(result, indent=4, ensure_ascii=False))
    out.close()


if __name__ == "__main__":
    main()
