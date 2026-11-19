"""
Demonstração da API de autenticação com JWT.

Executa todas as rotas usando o cliente de teste do Flask e imprime
o resultado de cada passo de forma organizada.

Uso (a partir da pasta api-jwt, com o venv ativo):
    python demo.py

Basta rodar e tirar um print da tela do terminal para anexar na atividade.
"""

import json
import sys
import warnings

# Garante que os acentos apareçam corretamente no terminal do Windows.
sys.stdout.reconfigure(encoding="utf-8")

# Silencia o aviso sobre o tamanho da chave secreta (usada apenas para a aula).
try:
    from jwt.warnings import InsecureKeyLengthWarning

    warnings.filterwarnings("ignore", category=InsecureKeyLengthWarning)
except Exception:
    pass

from app import app


def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


def mostrar(passo, metodo, rota, descricao, resposta):
    print(f"\n[{passo}] {metodo} {rota}  —  {descricao}")
    print(f"Status: {resposta.status_code}")
    try:
        print(json.dumps(resposta.get_json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resposta.get_data(as_text=True))


def main():
    cliente = app.test_client()

    titulo("DEMONSTRAÇÃO — API de Autenticação com JWT")

    # 1. Rota inicial
    mostrar(1, "GET", "/", "rota inicial", cliente.get("/"))

    # 2. Login com credenciais válidas
    login = cliente.post("/login", json={"usuario": "carolina", "senha": "1234"})
    mostrar(2, "POST", "/login", "login válido (carolina / 1234)", login)

    token = login.get_json()["access_token"]
    cabecalho = {"Authorization": f"Bearer {token}"}

    # 3. Rota protegida SEM token
    mostrar(3, "GET", "/perfil", "SEM token (deve dar 401)", cliente.get("/perfil"))

    # 4. Rota protegida COM token
    mostrar(4, "GET", "/perfil", "COM token (Bearer)", cliente.get("/perfil", headers=cabecalho))

    # 5. Desafio: área restrita
    mostrar(5, "GET", "/area-restrita", "COM token (Bearer)", cliente.get("/area-restrita", headers=cabecalho))

    # 6. Login com senha errada
    mostrar(6, "POST", "/login", "senha errada (deve dar 401)",
            cliente.post("/login", json={"usuario": "carolina", "senha": "errada"}))

    titulo("FIM DA DEMONSTRAÇÃO")


if __name__ == "__main__":
    main()
