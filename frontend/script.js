const url = "http://127.0.0.1:5000/livros";

const lista = document.getElementById("listaLivros");

const mensagem = document.getElementById("mensagem");

let editandoId = null;


async function carregarLivros() {

    const resposta = await fetch(url);

    const livros = await resposta.json();

    renderizarLivros(livros);
}



function renderizarLivros(livros) {

    lista.innerHTML = "";

    livros.forEach(livro => {

        lista.innerHTML += `
            <div class="card">

                <img src="${livro.imagem}" alt="Capa">

                <h2>${livro.titulo}</h2>

                <p><strong>Autor:</strong> ${livro.autor}</p>

                <p><strong>Categoria:</strong> ${livro.categoria}</p>

                <p><strong>Ano:</strong> ${livro.ano}</p>

                <p><strong>⭐ Avaliação:</strong> ${livro.avaliacao}</p>

                <p>${livro.descricao}</p>

                <div class="acoes">

                    <button onclick="editarLivro(${livro.id})">
                        Editar
                    </button>

                    <button class="delete"
                        onclick="deletarLivro(${livro.id})">
                        Excluir
                    </button>

                </div>

            </div>
        `;
    });
}



document
.getElementById("formLivro")
.addEventListener("submit", async function(e) {

    e.preventDefault();

    const livro = {

        titulo:
            document.getElementById("titulo").value,

        autor:
            document.getElementById("autor").value,

        categoria:
            document.getElementById("categoria").value,

        ano:
            document.getElementById("ano").value,

        avaliacao:
            document.getElementById("avaliacao").value,

        descricao:
            document.getElementById("descricao").value,

        imagem:
            document.getElementById("imagem").value
    };


    if(editandoId) {

        await fetch(`${url}/${editandoId}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(livro)
        });

        mensagem.innerHTML = "Livro atualizado!";

        editandoId = null;

    } else {

        await fetch(url, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(livro)
        });

        mensagem.innerHTML = "Livro cadastrado!";
    }

    document.getElementById("formLivro").reset();

    carregarLivros();
});



async function deletarLivro(id) {

    const confirmar =
        confirm("Deseja excluir este livro?");

    if(confirmar) {

        await fetch(`${url}/${id}`, {
            method: "DELETE"
        });

        mensagem.innerHTML = "Livro removido.";

        carregarLivros();
    }
}



async function editarLivro(id) {

    const resposta = await fetch(url);

    const livros = await resposta.json();

    const livro = livros.find(l => l.id === id);

    document.getElementById("titulo").value =
        livro.titulo;

    document.getElementById("autor").value =
        livro.autor;

    document.getElementById("categoria").value =
        livro.categoria;

    document.getElementById("ano").value =
        livro.ano;

    document.getElementById("avaliacao").value =
        livro.avaliacao;

    document.getElementById("descricao").value =
        livro.descricao;

    document.getElementById("imagem").value =
        livro.imagem;

    editandoId = id;
}



async function buscarLivros() {

    const busca =
        document.getElementById("campoBusca").value;

    const resposta =
        await fetch(`${url}?titulo=${busca}`);

    const livros = await resposta.json();

    renderizarLivros(livros);

    mensagem.innerHTML = "Busca realizada.";
}


carregarLivros();