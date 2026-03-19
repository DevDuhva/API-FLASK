from flask import Flask, jsonify
import os

app = Flask(__name__)

alunos = [
    {"id": 1, "nome": "Ana"},
    {"id": 2, "nome": "Carlos"},
    {"id": 3, "nome": "Carol"}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify(alunos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)