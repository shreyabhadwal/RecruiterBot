import LCMetaData
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(LCMetaData.print_answer2(userText))


if __name__ == "__main__":
    app.run()
#LCMetaData.print_answer2("Who is the best choice for php development")