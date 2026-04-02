from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = [
    {"id": 1, "nome": "Ana"},
    {"id": 2, "nome": "João"}
]

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    novo = request.json
    novo['id'] = len(usuarios) + 1
    usuarios.append(novo)
    return jsonify(novo), 201

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            dados = request.json
            usuario['nome'] = dados.get('nome', usuario['nome'])
            return jsonify(usuario)
    return {"erro": "Usuário não encontrado"}, 404

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            usuarios.remove(usuario)
            return {"mensagem": "Usuário removido"}
    return {"erro": "Usuário não encontrado"}, 404

if __name__ == '__main__':
    app.run(debug=True)
