// Defina sua paleta de cores
const paletaDeCores = ["#FFFFFF", "#0A0A0A", "#00D65D", "#6ED6DC", "#F3D84D", "#F348CE", "#AF35E4"];

// Função para gerar uma cor aleatória
function gerarCorAleatoria() {
  const corAleatoria = paletaDeCores[Math.floor(Math.random() * paletaDeCores.length)];
  return corAleatoria;
}

// Uso da função para gerar uma cor aleatória
const corHeader = gerarCorAleatoria();

// Aplique a cor à header usando CSS
document.querySelector(".header-do-usuario").style.backgroundColor = corHeader;
