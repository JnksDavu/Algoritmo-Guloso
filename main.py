import json

import re

def carregar_dados(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Remove caracteres de controle inválidos
    conteudo = re.sub(r"[\x00-\x1F\x7F]", "", conteudo)

    return json.loads(conteudo)


with open("cidadesSCDistâncias.json", "r", encoding="utf-8") as f:
    try:
        dados = json.load(f)
        print("JSON carregado com sucesso!")
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar JSON: {e}")


def encontrar_caminho_guloso(mapa, origem, destino):
    if origem not in mapa or destino not in mapa:
        return None, "Cidade de origem ou destino não encontrada."
    
    caminho = [origem]
    distancia_total = 0
    atual = origem
    visitadas = set()
    visitadas.add(origem)
    
    while atual != destino:
        vizinhos = [(cidade, dist) for cidade, dist in mapa[atual].items() if cidade not in visitadas]
        
        if not vizinhos:
            return None, "Não há caminho disponível para o destino."
        
        proxima_cidade, menor_distancia = min(vizinhos, key=lambda x: x[1])
        caminho.append(proxima_cidade)
        distancia_total += menor_distancia
        atual = proxima_cidade
        visitadas.add(proxima_cidade)
    
    return caminho, distancia_total

def main():
    arquivo_json = "cidadesSCDistâncias.json"  # Nome do arquivo JSON
    mapa = carregar_dados(arquivo_json)
    
    origem = input("Digite a cidade de origem: ")
    destino = input("Digite a cidade de destino: ")
    
    caminho, distancia = encontrar_caminho_guloso(mapa, origem, destino)
    
    if caminho:
        print("Caminho encontrado:", " -> ".join(caminho))
        print("Distância total percorrida:", distancia, "km")
    else:
        print("Erro:", distancia)

if __name__ == "__main__":
    main()