from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        req = request.form["fluid_name"]
        return render_template("index.html", result=req)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()
