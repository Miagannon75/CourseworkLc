from flask import Flask

app = Flask(__name__)

@app.route("/")
def hom():
    return "Flask is working properly"

app.run(host='0.0.0.0', port=6001, debug=False)
