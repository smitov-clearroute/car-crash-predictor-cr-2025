from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def race_map():
    return render_template("iframe.html")

if __name__ == "__main__":
    app.run(debug=True)
