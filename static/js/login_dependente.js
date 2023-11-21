    // Função genérica para fazer a chamada da API
async function chamarAPI(email) {
    try {
        const url = `logindependentes/${email}`;
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
    //const trs = document.querySelectorAll('tbody>tr');        
    //if (trs.length === 0) {
    window.location.href = 'inicialkids';
    //}
}


document.addEventListener('DOMContentLoaded', (event) => {
    const botoes = document.querySelectorAll('div.dependente');
    botoes.forEach((botao) => {
        botao.addEventListener('click', async (event) => {
            event.preventDefault();
            const email = botao.getAttribute('data-email');
            console.log(email)
            chamarAPI(email)
        });
    });
});