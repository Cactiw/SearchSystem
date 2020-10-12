
from service.query_service import parse_input, perform_query
from app import run_app

from Resources import Resources

import sys


def main():
    documents, words, vectors, max_words = parse_input()
    Resources.set_resources(documents, words, vectors, max_words)

    for arg in sys.argv[1:]:
        if arg == "--files-only":
            print("Generating files")

            for i, request in enumerate(Resources.requests):
                print("Writing {} request...".format(request))
                result = perform_query(request)
                result = list(filter(lambda res: res[1] > 0, result))

                s = "Запрос {}:\nРезультаты (название | коэффициент соответствия)\n\n" \
                    "{}".format(request, "\n".join(
                        list(map(lambda item: " | ".join(map(lambda elem: str(elem), item)), result))
                    ))

                with open("out/{}.txt".format(i + 1), encoding="utf-8", mode="w") as f:
                    f.write(s)

            print("Files generated, exiting.")
            return

    run_app()


if __name__ == "__main__":
    main()
