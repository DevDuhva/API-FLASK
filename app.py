from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

usuarios = [
    {
        "nome": "Ana Clara Souza",
        "email": "ana@email.com",
        "telefone": "(14) 99888-1111"
    },
    {
        "nome": "Lucas Oliveira",
        "email": "lucas@email.com",
        "telefone": "(14) 99777-2222"
    },
    {
        "nome": "Marina Costa",
        "email": "marina@email.com",
        "telefone": "(14) 99666-3333"
    }
]

@app.route("/")
def inicio():
    return "API funcionando!"

@app.route("/usuarios")
def listar_usuarios():
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(debug=True)