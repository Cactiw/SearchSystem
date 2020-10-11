
from flask import Flask, Response, request, abort, send_from_directory, send_file, render_template
from flask_cors import cross_origin, CORS

from service.query_service import perform_query, analyse_text, count_document_vector

from views.search_view import get_search_view

from model.SearchResult import SearchResult

from Resources import Resources

app = Flask(__name__)
CORS(app)


@app.route("/search/<query>")
def search(query: str):
    result = perform_query(query)
    table = get_search_view(list(filter(lambda res: res.coefficient > 0, map(lambda x: SearchResult(*x), result))))
    return render_template("search.html", table=table)


def run_app():
    app.run(host="0.0.0.0", port=5000)

