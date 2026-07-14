import requests
import csv

def buscar_pokemon(nome):
    print(f"Buscando {nome}...") ##ver qual pokemons esta consultando

    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

    resposta = requests.get(url, timeout=10) ##colocado timeout so para caso trave algo ele ficar no maximo 10 s

    if resposta.status_code != 200:        
        return None
    
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



    return pokemon

pokemons = []
pokemons_nao_encontrados = []

##Ler o csv
with open("pokemon_base.csv", "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        nome = linha["nome"].strip().lower() ##strip remove espaços antes e depois e lower deixa minusculos

        if nome == "":
            continue

        pokemon = buscar_pokemon(nome)

        if pokemon is not None:
            pokemons.append(pokemon)
        else:
            pokemons_nao_encontrados.append(nome)

# O que faremos para a primeira pergunta é
# procure dentro da lista pokemons o item cujo campo total_stats é o maior

maior_total = max(pokemons, key=lambda pokemon: pokemon["total_stats"]) ##se colocar na indentação errada ele vai calcular cada pokemon.. se por antes do loop a lista esta fazia.

## Resposta da Pergunta 1

print(
    f'1. Pokémon com maior soma total de stats: '
    f'{maior_total["nome"]} ({maior_total["total_stats"]})'
)


## Para a segunda pergunta vamos:
## 1. Criar um dicionário para agrupar ataques por tipo.
## 2. Para cada Pokémon:
##    - separar os tipos;
##    - para cada tipo, adicionar o attack daquele Pokémon.
## 3. Calcular a média de attack de cada tipo.
## 4. Encontrar o tipo com maior média.

ataques_por_tipo = {}

for pokemon in pokemons:
    tipos = pokemon["tipo(s)"].split(", ")

    for tipo in tipos:
        if tipo not in ataques_por_tipo:
            ataques_por_tipo[tipo] = []

        ataques_por_tipo[tipo].append(pokemon["attack"])


media_attack_por_tipo = {}

for tipo, ataques in ataques_por_tipo.items():
    media = sum(ataques) / len(ataques)
    media_attack_por_tipo[tipo] = media

tipo_maior_media = max(
    media_attack_por_tipo,
    key=lambda tipo: media_attack_por_tipo[tipo]
)

## Respota da Pergunta 2

print(
    f"2. Tipo com maior média de Attack: "
    f"{tipo_maior_media} ({media_attack_por_tipo[tipo_maior_media]:.2f})"
)

## Para a terceira pergunta vamos:
## 1. Começar contador em 0.
## 2. Para cada Pokémon:
##    - separar os tipos;
##    - verificar se "water" está na lista de tipos;
##    - se estiver, somar 1.

quantidade_water = 0

for pokemon in pokemons:
    tipos = pokemon["tipo(s)"].split(", ")

    if "water" in tipos:
        quantidade_water += 1

## Resposta da Pergunta 3

print(f"3. Quantidade de Pokémon do tipo Water: {quantidade_water}")

## Para responder a pergunta quatro
## Vamos precisar ordenar a lista pokemons pelo campo "speed" em ordem decrescente.

mais_rapidos = sorted(                      ##sorted  (pokemons ...  cria uma nova lista ordenada
    pokemons,
    key=lambda pokemon: pokemon["speed"],    ## diz que o criterio de ordenação é o campo speed
    reverse=True                               ## ordena do maior para o menor
)

top_5_rapidos = mais_rapidos[:5]            ##mais_rapidos[:5] pega só os 5 primeiros

## Resposta da Pergunta 4

print("4. Top 5 mais rápidos:")
for pokemon in top_5_rapidos:
    print(pokemon["nome"], pokemon["speed"])

##  A quinta pergunta é proximo da quartam veja:
## sorted(...) cria uma lista ordenada
## key=lambda pokemon: pokemon["total_stats"] diz que a ordenação deve usar o campo total_stats
## reverse=True coloca do maior para o menor
## [:6] pega só os 6 primeiros

time_dos_sonhos = sorted(pokemons, key=lambda pokemon: pokemon["total_stats"], reverse=True)

top_6_time = time_dos_sonhos[:6]

## Resposta da Pergunta 5

print("5. Time dos sonhos com maior soma de stats:")
for pokemon in top_6_time:
    print(pokemon["nome"], pokemon["total_stats"])


# Montar o arquivo CSV
colunas = [
    "nome",
    "tipo(s)",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
    "altura",
    "peso",
    "habilidade(s)",
    "total_stats"
]

with open("pokemon_completo.csv", "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=colunas) ##fieldnames=colunas define a ordem das colunas 
    ##Como pokemons é uma lista de dicionários, dá para salvar com csv.DictWriter.
    escritor.writeheader() ## writeheader escreve o cabeçalho
    escritor.writerows(pokemons)  ##writerows(pokemons) escreve todos os dicionarios da lista

# Montar o arquivo TXT
respostas = []

respostas.append(
    f"1. Pokémon com maior soma total de stats: {maior_total['nome']} ({maior_total['total_stats']})"
)

respostas.append(
    f"2. Tipo com maior média de Attack: {tipo_maior_media} ({media_attack_por_tipo[tipo_maior_media]:.2f})"
)

respostas.append(
    f"3. Quantidade de Pokémon do tipo Water: {quantidade_water}"
)

respostas.append("4. Top 5 mais rápidos:")
for pokemon in top_5_rapidos:
    respostas.append(f"{pokemon['nome']} {pokemon['speed']}")

respostas.append("5. Time dos sonhos com maior soma de stats:")
for pokemon in top_6_time:
    respostas.append(f"{pokemon['nome']} {pokemon['total_stats']}")

with open("respostas.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("\n".join(respostas))


## Somente para mostrar quais pokemons nao foram buscados e nao fizeram parte da pesquisa

if pokemons_nao_encontrados:
    print("Pokémons que não fizeram parte da pesquisa pois não foram encontrados:", ", ".join(pokemons_nao_encontrados))
else:
    print("Todos os Pokémon foram encontrados.")