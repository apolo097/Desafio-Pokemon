const botaoCarregar = document.getElementById("botaoCarregar");
const tabelaPokemons = document.getElementById("tabelaPokemons");

botaoCarregar.addEventListener("click", carregarPokemons);

function carregarPokemons() {
  fetch("pokemon_completo.csv")
    .then(function (resposta) {
      return resposta.text();
    })
    .then(function (textoCsv) {
      const linhas = textoCsv.split("\n");

      tabelaPokemons.innerHTML = "";

      for (let i = 1; i < linhas.length; i++) {
        const linha = linhas[i];

        if (linha.trim() === "") {
          continue;
        }

        const colunas = separarLinhaCsv(linha);

        const nome = colunas[0];
        const tipos = colunas[1];
        const hp = colunas[2];
        const attack = colunas[3];
        const defense = colunas[4];
        const speed = colunas[7];
        const total = colunas[11];

        const tr = document.createElement("tr");

        tr.innerHTML = `
          <td>${nome}</td>
          <td>${tipos}</td>
          <td>${hp}</td>
          <td>${attack}</td>
          <td>${defense}</td>
          <td>${speed}</td>
          <td>${total}</td>
        `;

        tabelaPokemons.appendChild(tr);
      }
    });
}

function separarLinhaCsv(linha) {
  const colunas = [];
  let valorAtual = "";
  let dentroDeAspas = false;

  for (let i = 0; i < linha.length; i++) {
    const caractere = linha[i];

    if (caractere === '"') {
      dentroDeAspas = !dentroDeAspas;
    } else if (caractere === "," && dentroDeAspas === false) {
      colunas.push(valorAtual);
      valorAtual = "";
    } else {
      valorAtual += caractere;
    }
  }

  colunas.push(valorAtual);

  return colunas;
}