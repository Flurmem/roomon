// Função genérica para fazer a chamada da API
async function chamarAPI(id, idSeguido, opcao) {
    try {
        const url = `/perfilkids/${id}/${idSeguido}/${opcao}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        recarregarPagina();

    } catch (error) {
        console.error('Erro ao chamar a API:', error);
    }
}

function recarregarPagina() {
    window.location.reload()
}

// Adicionar um evento de clique a todos os elementos <button> com classe "seguir"
document.addEventListener('DOMContentLoaded', (event) => {
    const botoes = document.querySelectorAll('button.seguir');
    botoes.forEach((botao) => {
        botao.addEventListener('click', async (event) => {
            event.preventDefault();
            const id = botao.getAttribute('data-id');
            const idSeguido = botao.getAttribute('value');
            const excluir = Boolean(botao.getAttribute('excluir'));
            const bloquear = Boolean(botao.getAttribute('bloquear'));

            if (excluir) {
                await chamarAPI(id, idSeguido, 'excluir');
            } else if (bloquear) {
                await chamarAPI(id, idSeguido, 'bloquear');
            } else {
                await chamarAPI(id, idSeguido, 'seguir');
            }
            recarregarPagina()
        });
    });
});
