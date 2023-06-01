# use maximum 8 workers for wsgi
from flask import Flask, Response
import gunicorn

app = Flask(__name__)


@app.route('/')
def test_root():
    return Response(status=200)

# gunicorn --workers=8 src.web.python.test_flask:app