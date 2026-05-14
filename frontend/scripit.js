const botao = document.getElementById("btnUsuarios");
const areaUsuarios = document.getElementById("usuarios");

botao.addEventListener("click", buscarUsuarios);

function buscarUsuarios(){

    fetch("https://api-flask-2-qjhw.onrender.com/usuarios")

    .then(resposta => resposta.json())

    .then(dados => {

        areaUsuarios.innerHTML = "";

        dados.forEach(usuario => {

            areaUsuarios.innerHTML += `
            
                <div class="card">

                    <h2>${usuario.nome}</h2>

                    <p><strong>Email:</strong> ${usuario.email}</p>

                    <p><strong>Telefone:</strong> ${usuario.telefone}</p>

                </div>

            `;
        });

    })

    .catch(erro => {
        areaUsuarios.innerHTML =
        "<p>Erro ao carregar usuários.</p>";

        console.log(erro);
    });

}