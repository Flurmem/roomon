
//Abrir modal
    const myModal = document.getElementById('myModal')
    const myInput = document.getElementById('myInput')

    myModal.addEventListener('shown.bs.modal', () => {
        myInput.focus()
    })



//Tooltip
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));

    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });



//Salvar e editar
    function alterarBotao() {
        var botao = document.getElementById("btnEditar");
        if (botao.textContent == "Salvar") {
            var icone = `
            <svg xmlns=" http://www.w3.org/2000/svg" width="25" height="25"
            fill="currentColor" class="bi bi-pencil-square me-1"
            viewBox="0 0 16 16">
            <path
                d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
            <path fill-rule="evenodd"
                d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
            </svg>
        `
            botao.innerHTML =  icone + "Editar";
            botao.className = "btn";
            botao.style.backgroundColor='gray';
            
        } else {
            botao.textContent = "Salvar";
            botao.className = "btn";
            botao.style.backgroundColor='green'; // Altera a classe para uma cor diferente (verde)
        }
    }
            
    function mudarImagemCarrossel() {
        // Obtém todas as imagens do carrossel
        var carouselImages = document.querySelectorAll('#carousel_criadores_bloqueados .carousel-item img');

        // Aplica blur em todas as imagens
        carouselImages.forEach(function(image) {
            image.style.filter = 'blur(1px)';
        });

        // Adiciona ícone de lixeira em cada imagem
        carouselImages.forEach(function(image) {
            var trashIcon = document.createElement('i');
            trashIcon.classList.add('fas', 'fa-trash', 'position-absolute', 'trash-icon');
            trashIcon.style.top = '50%';
            trashIcon.style.left = '50%';
            trashIcon.style.transform = 'translate(-50%, -50%)';
            image.parentElement.appendChild(trashIcon);
        });
    }

        // Adicionar um evento de clique ao botão para chamar a função
        //document.getElementById('btnEditar').addEventListener('click', mudarImagemCarrossel);

        function mudarImagemPerfil() {
            var image = document.getElementById('imagemPerfil');
            image.style.filter = 'blur(2px)';
            var icon = document.createElement('i');
            icon.classList.add('bi', 'bi-pencil-fill', 'position-absolute'); // Exemplo de um ícone de estrela
            icon.style.position = 'absolute';
            icon.style.top = '24%';
            icon.style.left = '17%';
            icon.style.transform = 'translate(-50%, -50%)';
            icon.style.color = 'black';
            icon.style.fontSize = '30px';
            image.parentElement.appendChild(icon); // Adicione o ícone ao elemento pai da imagem
        }
        //document.getElementById('btnEditar').addEventListener('click', mudarImagemPerfil);

        function aceitarEdicao() {
            var descricao = document.getElementById("descricao");
            descricao.removeAttribute("disabled");
            descricao.removeAttribute("readonly");
            descricao.classList.replace("bg-dark", "bg-light");

            var usuario = document.getElementById("usuario");
            usuario.removeAttribute("disabled");
            usuario.removeAttribute("readonly");
            usuario.classList.replace("bg-dark", "bg-light");
    
            var apelido = document.getElementById("apelido");
            apelido.removeAttribute("disabled");
            apelido.removeAttribute("readonly");
            apelido.classList.replace("bg-dark", "bg-light");
    
            var nomeCompleto = document.getElementById("nomeCompleto");
            nomeCompleto.removeAttribute("disabled");
            nomeCompleto.removeAttribute("readonly");
            nomeCompleto.classList.replace("bg-dark", "bg-light");
    
            var email = document.getElementById("email");
            email.removeAttribute("disabled");
            email.removeAttribute("readonly");
            email.classList.replace("bg-dark", "bg-light");
    
            var data_nasc = document.getElementById("data_nasc");
            data_nasc.removeAttribute("disabled");
            data_nasc.removeAttribute("readonly");
            data_nasc.classList.replace("bg-dark", "bg-light");
    
            var senha = document.getElementById("senha");
            senha.removeAttribute("disabled");
            senha.removeAttribute("readonly");
            senha.classList.replace("bg-dark", "bg-light");

            var leitura = document.getElementById("leitura");
            leitura.removeAttribute("disabled");
            

            var arte = document.getElementById("arte");
            arte.removeAttribute("disabled");
            

            var conversa = document.getElementById("conversa");
            conversa.removeAttribute("disabled");

            var musica = document.getElementById("musica");
            musica.removeAttribute("disabled");

            var jogos = document.getElementById("jogos");
            jogos.removeAttribute("disabled");

            var escola = document.getElementById("escola");
            escola.removeAttribute("disabled");

            var danca = document.getElementById("danca");
            danca.removeAttribute("disabled");
            
            
        }
        //document.getElementById('btnEditar').addEventListener('click', aceitarEdicao);
        
        function voltarImagemCarrossel() {
            // Obtém todas as imagens do carrossel
            var carouselImages = document.querySelectorAll('#carousel_criadores_bloqueados .carousel-item img');

            // Aplica blur em todas as imagens
            carouselImages.forEach(function(image) {
                image.style.filter = 'none';
            });

            // Adiciona ícone de lixeira em cada imagem
        }

            // Adicionar um evento de clique ao botão para chamar a função
            //document.getElementById('btnEditar').addEventListener('click', voltarImagemCarrossel);

        function voltarImagemPerfil() {
            var image = document.getElementById('imagemPerfil');
            image.style.filter = 'none';
            
        }
    

    //finalizar as funções inversas
        function editarModal() {
            var botao = document.getElementById("btnEditar");
            if (botao.textContent == "Salvar"){
                //negarEdicao()
                //voltarBotao()
                //voltarImagemPerfil()
                voltarImagemCarrossel()
            }
            else {
                aceitarEdicao()
                alterarBotao()
                mudarImagemPerfil()
                mudarImagemCarrossel()

           }
        }


    var senhaInput = document.getElementById("senha");
    var toggleSenhaButton = document.getElementById("toggleSenha");

    
    toggleSenhaButton.addEventListener("click", function() {
        if (senhaInput.type === "password") {
            senhaInput.type = "text";
            toggleSenhaButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-eye-slash-fill" viewBox="0 0 16 16"><path d="m10.79 12.912-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7.029 7.029 0 0 0 2.79-.588zM5.21 3.088A7.028 7.028 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474L5.21 3.089z"/><path d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829l-2.83-2.829zm4.95.708-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6-12-12 .708-.708 12 12-.708.708z"/></svg>';
        } else {
            senhaInput.type = "password";
            toggleSenhaButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-eye-fill" viewBox="0 0 16 16"><path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/><path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/></svg>';
        }
    });

//Alterar assinatura

function alterarAssinatura() {
    var nomeAssinante = document.getElementById("nomeAssinante");
    nomeAssinante.removeAttribute("disabled");
    nomeAssinante.removeAttribute("readonly");
    nomeAssinante.classList.replace("bg-dark", "bg-light");

    var cpf = document.getElementById("cpf");
    cpf.removeAttribute("disabled");
    cpf.removeAttribute("readonly");
    cpf.classList.replace("bg-dark", "bg-light");

    var data_nascAssinante = document.getElementById("data_nascAssinante");
    data_nascAssinante.removeAttribute("disabled");
    data_nascAssinante.removeAttribute("readonly");
    data_nascAssinante.replace("bg-dark", "bg-light");

    var data_renovacao = document.getElementById("data_renovacao");
    data_renovacao.removeAttribute("disabled");
    data_renovacao.removeAttribute("readonly");
    data_renovacao.classList.replace("bg-dark", "bg-light");

    var valor = document.getElementById("valor");
    valor.removeAttribute("disabled");
    valor.removeAttribute("readonly");
    valor.classList.replace("bg-dark", "bg-light");

    document.getElementById('alterarAssinatura').addEventListener('click', alterarAssinatura);
}
