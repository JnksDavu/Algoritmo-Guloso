import json

def carregar_dados(caminho_arquivo):
    """Carrega o mapa de cidades a partir de um arquivo JSON."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado!")
        return None
    except json.JSONDecodeError:
        print("Erro: Falha ao decodificar o arquivo JSON!")
        return None

def encontrar_proximo_destino(vizinhos_disponiveis):
    """Encontra o vizinho mais próximo com base na menor distância."""
    return min(vizinhos_disponiveis, key=vizinhos_disponiveis.get)

def algoritmo_guloso(mapa_cidades, origem, destino):
    """Executa o algoritmo guloso para encontrar o menor caminho entre origem e destino."""
    caminho, cidades_visitadas = [], set()
    cidade_atual, distancia_total, logs = origem, 0, []
    
    logs.append(f"[INÍCIO] Buscando rota de {origem} para {destino}...")
    
    while cidade_atual != destino:
        if cidade_atual not in mapa_cidades:
            logs.append(f"[ERRO] Cidade {cidade_atual} não encontrada no mapa!")
            return None, None, logs
        
        caminho.append(cidade_atual)
        cidades_visitadas.add(cidade_atual)
        logs.append(f"[VISITA] Cidade atual: {cidade_atual}")
        
        vizinhos_disponiveis = {c: d for c, d in mapa_cidades[cidade_atual].items() if c not in cidades_visitadas}
        logs.append(f"[OPÇÕES] Vizinhos disponíveis: {', '.join(f'{c} ({d} km)' for c, d in vizinhos_disponiveis.items())}")
        
        if destino in vizinhos_disponiveis:
            distancia_total += vizinhos_disponiveis[destino]
            caminho.append(destino)
            logs.append(f"[SUCESSO] Destino {destino} encontrado! Distância total: {distancia_total} km")
            return caminho, distancia_total, logs
        
        if not vizinhos_disponiveis:
            logs.append("[FALHA] Nenhum caminho disponível - rota impossível!")
            return None, None, logs
        
        proxima_cidade = encontrar_proximo_destino(vizinhos_disponiveis)
        distancia_total += vizinhos_disponiveis[proxima_cidade]
        
        logs.append(f"[DECISÃO] Próxima cidade: {proxima_cidade} (Menor distância: {vizinhos_disponiveis[proxima_cidade]} km)")
        logs.append(f"[PROGRESSO] Distância acumulada: {distancia_total} km")
        
        cidade_atual = proxima_cidade
        
        if len(caminho) > len(mapa_cidades):
            logs.append("[ERRO] Número máximo de cidades excedido - possível loop detectado!")
            return None, None, logs
    
    return caminho, distancia_total, logs

def main():
    caminho_arquivo = 'cidadesSCDistâncias.json'
    mapa_cidades = carregar_dados(caminho_arquivo)
    if not mapa_cidades:
        return
    
    origem = input("Cidade de origem: ").strip()
    destino = input("Cidade de destino: ").strip()
    
    if origem not in mapa_cidades:
        print(f"[ERRO] Cidade de origem '{origem}' não encontrada!")
        return
    if destino not in mapa_cidades:
        print(f"[ERRO] Cidade de destino '{destino}' não encontrada!")
        return
    
    caminho, distancia_total, logs = algoritmo_guloso(mapa_cidades, origem, destino)
    
    print("\n=== LOG DE EXECUÇÃO ===")
    for log in logs:
        print(log)
    
    if not caminho:
        print(f"\n[RESULTADO] Não foi possível encontrar um caminho entre {origem} e {destino}.")
        return
    
    print("\n=== ROTA FINAL ===")
    for i in range(len(caminho) - 1):
        print(f"{caminho[i]} -> {caminho[i+1]}: {mapa_cidades[caminho[i]][caminho[i+1]]} km")
    
    print(f"\nDistância total percorrida: {distancia_total} km")

if __name__ == "__main__":
    main()