from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)

chatbot = Chatbot("data/knowledge.json")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "response": "Please enter a message."
        })

    response = chatbot.get_response(user_message)

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(debug=True)