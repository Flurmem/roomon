const slideDuration = 1000;
const reverseSlideDuration = 2000;

const btn_crianca = document.getElementById('btn_crianca');
const btn_categorias = document.getElementById('btn_categorias');

const rtn_crianca = document.getElementById('rtn_crianca');
const rtn_adulto = document.getElementById('rtn_adulto');

const container_adulto = document.getElementById('section_adulto');
const container_crianca = document.getElementById('section_crianca');
const container_categorias = document.getElementById('section_categorias');

function slideIn(fromContainer, toContainer) {
  fromContainer.classList.remove('slide-in-left');
  fromContainer.classList.add('slide-in-right');
  
  setTimeout(() => {
    fromContainer.style.display = 'none';
    toContainer.style.display = 'block';
    toContainer.classList.add('slide-in-left');
  
    fromContainer.classList.remove('slide-in-right');
    fromContainer.classList.add('slide-in-right--reverse');
  }, slideDuration);
  
  setTimeout(() => {
    toContainer.classList.remove('slide-in-left');
  }, reverseSlideDuration);
}

btn_crianca.addEventListener('click', () => {
  slideIn(container_adulto, container_crianca);
});

btn_categorias.addEventListener('click', () => {
  slideIn(container_crianca, container_categorias);
});

function reverseSlideIn(fromContainer, toContainer) {
  fromContainer.classList.add('slide-in-left--reverse');
  setTimeout(() => {
    fromContainer.style.display = 'none';
    toContainer.classList.add('slide-in-right--reverse');
    toContainer.style.display = 'block';
    fromContainer.classList.remove('slide-in-left--reverse');
  }, slideDuration);
  
  setTimeout(() => {
    toContainer.classList.remove('slide-in-right--reverse');
  }, reverseSlideDuration);
}

rtn_adulto.addEventListener('click', () => {
  reverseSlideIn(container_crianca, container_adulto);
});

rtn_crianca.addEventListener('click', () => {
  reverseSlideIn(container_categorias, container_crianca);
});
