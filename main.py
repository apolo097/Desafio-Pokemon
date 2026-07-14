import requests

url = "https://pokeapi.co/api/v2/pokemon/charizard"

resposta = requests.get(url)
dados = resposta.json()

print("Nome:", dados["name"])

print("\nTipos:")
for item in dados["types"]:
    print(item["type"]["name"])

print("\nHabilidades:")
for item in dados["abilities"]:
    print(item["ability"]["name"])

print("\nStats:")
for item in dados["stats"]:
    nome_stat = item["stat"]["name"]
    valor_stat = item["base_stat"]

    print(nome_stat, valor_stat)

    ##Só para analisarmos que dentro do padrão python temos item ["type"]["name"] -> dentro de item pegue type e dentro de type pegue name.