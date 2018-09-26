from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'index2222222222'


if __name__ == '__main__':
    app.run(debug=True)
