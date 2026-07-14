import requests

url = "https://pokeapi.co/api/v2/pokemon/charizard"

resposta = requests.get(url)
dados = resposta.json()

tipos = []
for item in dados["types"]:
    tipos.append(item["type"]["name"])

habilidades = []
for item in dados["abilities"]:
    habilidades.append(item["ability"]["name"])

stats = {}
for item in dados["stats"]:
    nome_stat = item["stat"]["name"]
    valor_stat = item["base_stat"]
    stats[nome_stat] = valor_stat

## print(stats) -> caso queira ver que aqui ele esta juntando em uma lista todos juntos. Como se eu criasse outro json de dados. Idem ao que vem da api por exemplo. ai temos dados e stats

pokemon = {    
    "nome": dados["name"],
    "tipo(s)": ", ".join(tipos),
    "hp": stats["hp"],
    "attack":stats["attack"],
    "defense":stats["defense"],
    "special_attack":stats["special-attack"],
    "special_defense":stats["special-defense"],
    "speed":stats["speed"],
    "altura":dados["height"]/10,
    "peso":dados["weight"]/10, ##dividido por 10 para ficar em medidas humanas
    "habilidade(s)": ", ".join(habilidades),
    "total_stats":sum(stats.values())
}


print(pokemon)

