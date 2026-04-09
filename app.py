from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        "id": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899
    },
    {
        "id": 2,
        "titulo": "O Hobbit",
        "autor": "J.R.R. Tolkien",
        "ano": 1937
    },
    {
        "id": 3,
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949
    },
    {
        "id": 4,
        "titulo": "A Revolução dos Bichos",
        "autor": "George Orwell",
        "ano": 1945
    }
]

@app.route('/')
def home():
    return {
        "mensagem": "API Biblioteca funcionando",
        "rotas": {
            "GET /livros": "Listar livros",
            "GET /livros/<id>": "Buscar livro por id",
            "POST /livros": "Cadastrar livro",
            "PUT /livros/<id>": "Atualizar livro",
            "DELETE /livros/<id>": "Deletar livro"
        }
    }

@app.route('/livros', methods=['GET'])
def listar_livros():
    return jsonify(livros)

@app.route('/livros/<int:id>', methods=['GET'])
def buscar_livro(id):
    for livro in livros:
        if livro['id'] == id:
            return jsonify(livro)
    return {"erro": "Livro não encontrado"}, 404

@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    dados = request.json

    if not dados.get('titulo') or not dados.get('autor'):
        return {"erro": "Título e autor são obrigatórios"}, 400

    if 'ano' in dados and dados['ano'] < 0:
        return {"erro": "Ano inválido"}, 400

    for l in livros:
        if l['titulo'].lower() == dados['titulo'].lower():
            return {"erro": "Livro já cadastrado"}, 400

    novo_livro = {
        "id": len(livros) + 1,
        "titulo": dados['titulo'],
        "autor": dados['autor'],
        "ano": dados.get('ano', None)
    }

    livros.append(novo_livro)

    return {
        "mensagem": "Livro cadastrado com sucesso",
        "livro": novo_livro
    }, 201

@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    for livro in livros:
        if livro['id'] == id:
            dados = request.json

            if 'ano' in dados and dados['ano'] < 0:
                return {"erro": "Ano inválido"}, 400

            livro['titulo'] = dados.get('titulo', livro['titulo'])
            livro['autor'] = dados.get('autor', livro['autor'])
            livro['ano'] = dados.get('ano', livro['ano'])

            return {
                "mensagem": "Livro atualizado com sucesso",
                "livro": livro
            }

    return {"erro": "Livro não encontrado"}, 404

@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    for livro in livros:
        if livro['id'] == id:
            livros.remove(livro)
            return {"mensagem": "Livro removido com sucesso"}

    return {"erro": "Livro não encontrado"}, 404

if __name__ == '__main__':
    app.run(debug=True)
