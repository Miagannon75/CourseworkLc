from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    # Single variable to render
    message = "Hello, Flask1!"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)