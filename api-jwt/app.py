from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-secreta-da-aula"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)

# Dicionário usado como "banco de dados" de exemplo.
# As senhas são armazenadas como hash, nunca em texto puro.
usuarios = {
    "carolina": {
        "nome": "Carolina Cardinale",
        "senha": generate_password_hash("1234"),
        "perfil": "professora",
    },
    "ana": {
        "nome": "Ana Souza",
        "senha": generate_password_hash("abcd"),
        "perfil": "aluna",
    },
}


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"mensagem": "API de autenticação com JWT"}), 200


@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie os dados em formato JSON"}), 400

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"erro": "Informe o usuário e a senha"}), 400

    usuario_encontrado = usuarios.get(usuario)
    if not usuario_encontrado:
        return jsonify({"erro": "Usuário ou senha inválidos"}), 401

    senha_correta = check_password_hash(usuario_encontrado["senha"], senha)
    if not senha_correta:
        return jsonify({"erro": "Usuário ou senha inválidos"}), 401

    token = create_access_token(identity=usuario)

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "access_token": token,
    }), 200


@app.route("/perfil", methods=["GET"])
@jwt_required()
def consultar_perfil():
    usuario_atual = get_jwt_identity()
    dados_usuario = usuarios.get(usuario_atual)

    return jsonify({
        "usuario": usuario_atual,
        "nome": dados_usuario["nome"],
        "perfil": dados_usuario["perfil"],
    }), 200


@app.route("/area-restrita", methods=["GET"])
@jwt_required()
def area_restrita():
    usuario_atual = get_jwt_identity()
    return jsonify({
        "mensagem": f"Bem-vindo à área restrita, {usuario_atual}!"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
