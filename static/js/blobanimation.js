    const bolinhas = document.getElementsByClassName('circulo');

    Array.from(bolinhas).forEach(bolinha => {
      bolinha.addEventListener('mouseover', function () {
        bolinha.style.cursor = 'pointer'
        bolinha.classList.add('blob')
      }),
        bolinha.addEventListener('animationend', function () {
          bolinha.classList.remove('blob');

        })
    });