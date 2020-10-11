
from flask import Flask, Response, request, abort, send_from_directory, send_file, render_template
from flask_cors import cross_origin, CORS

from service.query_service import perform_query, analyse_text, count_document_vector

from Resources import Resources

app = Flask(__name__)
CORS(app)


@app.route("/search/<query>")
def search(query: str):
    return str(perform_query(query))


def run_app():
    app.run(host="0.0.0.0", port=5000)

