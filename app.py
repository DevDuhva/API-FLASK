from flask import Flask, jsonify, request
import os

app = Flask(__name__)

usuarios = [
    {"id": 1, "nome": "Ana"},
    {"id": 2, "nome": "Carlos"},
    {"id": 3, "nome": "Carol"}
]

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(usuarios)

@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    novo = request.json
    novo['id'] = len(usuarios) + 1
    usuarios.append(novo)
    return jsonify(novo), 201  

if __name__ == "__main__":
    app.run(debug=True)
