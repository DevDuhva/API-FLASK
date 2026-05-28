from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

livros = [
    {
        "id": 1,
        "titulo": "O Hobbit",
        "autor": "Tolkien",
        "categoria": "Fantasia",
        "ano": 1937,
        "avaliacao": 5,
        "descricao": "Uma aventura épica.",
        "imagem": "https://m.media-amazon.com/images/I/91b0C2YNSrL.jpg"
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/livros", methods=["GET"])
def listar_livros():
    titulo = request.args.get("titulo")

    if titulo:
        filtrados = [
            livro for livro in livros
            if titulo.lower() in livro["titulo"].lower()
        ]
        return jsonify(filtrados)

    return jsonify(livros)


@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.json

    novo = {
        "id": len(livros) + 1,
        "titulo": dados["titulo"],
        "autor": dados["autor"],
        "categoria": dados["categoria"],
        "ano": dados["ano"],
        "avaliacao": dados["avaliacao"],
        "descricao": dados["descricao"],
        "imagem": dados["imagem"]
    }

    livros.append(novo)

    return jsonify(novo), 201

@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livro(id):
    dados = request.json

    for livro in livros:
        if livro["id"] == id:
            livro["titulo"] = dados["titulo"]
            livro["autor"] = dados["autor"]
            livro["categoria"] = dados["categoria"]
            livro["ano"] = dados["ano"]
            livro["avaliacao"] = dados["avaliacao"]
            livro["descricao"] = dados["descricao"]
            livro["imagem"] = dados["imagem"]

            return jsonify(livro)

    return jsonify({"erro": "Livro não encontrado"}), 404


@app.route("/livros/<int:id>", methods=["DELETE"])
def deletar_livro(id):
    global livros

    livros = [livro for livro in livros if livro["id"] != id]

    return jsonify({"mensagem": "Livro removido"})

if __name__ == "__main__":
    app.run(debug=True)