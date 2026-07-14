import csv
import requests

##Leu o csv
with open("pokemon_base.csv", "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        print(linha)




##Chamei a API e peguei campos simples.
url = "https://pokeapi.co/api/v2/pokemon/charizard"

resposta = requests.get(url)

dados = resposta.json()

print("Nome:", dados["name"])
print("Altura:", dados["height"])
print("Peso:", dados["weight"])