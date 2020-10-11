
from service.query_service import parse_input

from controller.app import run_app

from Resources import Resources

PROCESS_NUM = 4


def main():
    documents, words, vectors = parse_input()
    Resources.set_resources(documents, words, vectors)

    run_app()


if __name__ == "__main__":
    main()
