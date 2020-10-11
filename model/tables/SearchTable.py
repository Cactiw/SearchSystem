
from flask_table import Table, Col


class SearchTable(Table):
    title = Col('Title')
    coefficient = Col('Coefficient')
