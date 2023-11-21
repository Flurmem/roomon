const elementos = document.querySelectorAll('.elemento');

elementos.forEach(elemento => {
    const linha = elemento.querySelector('.linha');

    elemento.addEventListener('mouseover', () => {
        linha.style.transform = 'scaleX(1)'; // Expandir a linha
    });

    elemento.addEventListener('mouseout', () => {
        linha.style.transform = 'scaleX(0)'; // Ocultar a linha
    });
});