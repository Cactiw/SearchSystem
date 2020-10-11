
from model.tables.SearchTable import SearchTable


def get_search_view(result: list):
    table = SearchTable(result, border=True)
    return table
