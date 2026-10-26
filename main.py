# ============ IMPORTS ============
import csv  # 🔒 biblioteca do Python para ler arquivos .csv
import re #  🔒 biblioteca do Python para expressões regulares (regex)


# ============ FUNÇÕES ============

# CÓDIGO DO SPRINT 1 (Leitura do arquivo)
def carregar_dados(caminho):  # ✏️ "caminho" = nome do arquivo que vamos abrir
    # 🔒 open abre o arquivo; "with" fecha sozinho no final
    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        # 🔒 DictReader lê cada linha como um dicionário: {coluna: valor}
        leitor = csv.DictReader(arquivo)
        # devolve todos os pedidos numa lista (o leitor só pode ser lido uma vez)
        return list(leitor)


def mostrar_primeiros(registros, quantidade=3):  # ✏️ padrão: mostra 3
    # 🔒 enumerate numera os pedidos: 1, 2, 3...
    for numero, registro in enumerate(registros[:quantidade], start=1):
        print(f"\n--- Registro {numero} ---")
        # cada pedido é um dicionário; .items() dá "coluna" e "valor"
        for coluna, valor in registro.items():
            # {valor!r} mostra entre aspas, para enxergar espaços escondidos
            print(f"{coluna}: {valor!r}")

def valores_distintos(registros, coluna):
    # set = conjunto: guarda cada valor uma vez só, sem repetir
    encontrados = set()
    for registro in registros:
        # registro[coluna] pega o valor daquela coluna neste pedido
        encontrados.add(registro[coluna])
    # sorted coloca em ordem alfabética para facilitar a leitura
    return sorted(encontrados)


def limpar_categoria(texto):
    # 1) tira os espaços das pontas
    limpo = texto.strip()
    # 2) deixa tudo minúsculo
    limpo = limpo.lower()
    # 3) apaga o que NÃO é letra a-z nem espaço (some o "!!!")
    limpo = re.sub(r"[^a-z\s]", "", limpo)
    # 4) se não sobrou nada, marca como "sem categoria"
    if limpo == "":
        limpo = "sem categoria"
    return limpo


def padronizar_categorias(registros):
    vazias_preenchidas = 0
    nao_vazias_alteradas = 0
    for registro in registros:
        original = registro["categoria"]
        novo = limpar_categoria(original)
        # conta cada caso separadamente
        if original.strip() == "":
            vazias_preenchidas += 1
        elif novo != original:
            nao_vazias_alteradas += 1
        # guarda o texto original e troca pela versão limpa
        registro["categoria_original"] = original
        registro["categoria"] = novo
    # devolve os dois números
    return vazias_preenchidas, nao_vazias_alteradas

# tabelinha: texto limpo -> nome oficial do canal
CANAIS_OFICIAIS = {
    "mercado": "Mercado",
    "web": "Web",
    "loja física": "Loja física",
    "loja fisica": "Loja física",  # caso venha sem acento
}


def padronizar_canal(texto):
    # tira espaços das pontas, deixa minúsculo e junta espaços repetidos
    chave = re.sub(r"\s+", " ", texto.strip().lower())
    # se está na tabelinha: (reconheceu = True, nome oficial)
    if chave in CANAIS_OFICIAIS:
        return True, CANAIS_OFICIAIS[chave]
    # se não está: (reconheceu = False, texto como veio)
    return False, texto

def padronizar_canais(registros):
    corrigidos = 0
    nao_reconhecidos = 0
    for registro in registros:
        original = registro["canal_venda"]
        reconheceu, oficial = padronizar_canal(original)
        # guarda o texto original de qualquer jeito
        registro["canal_original"] = original
        if reconheceu:
            # conta só se o nome realmente mudou
            if oficial != original:
                corrigidos += 1
            registro["canal_venda"] = oficial
        else:
            # não reconheceu: conta e deixa como veio
            nao_reconhecidos += 1
    # devolve os dois números
    return corrigidos, nao_reconhecidos

def validar_quantidade(texto):
    # tenta transformar em número inteiro
    try:
        valor = int(texto.strip())
    except ValueError:
        # vazio ou texto: não converte, então é problema
        return False, "não é um número inteiro"
    # regra de negócio: precisa ser maior que zero
    if valor <= 0:
        return False, "quantidade menor ou igual a zero"
    return True, valor


def validar_preco(texto):
    # tenta transformar em número decimal (116.6)
    try:
        valor = float(texto.strip())
    except ValueError:
        # vazio ou texto: não converte, então é problema
        return False, "não é um número"
    # regra de negócio: preço não pode ser negativo
    if valor < 0:
        return False, "preço negativo"
    return True, valor

# ============ EXECUÇÃO ============
# 📄 lê o arquivo e guarda os 1500 pedidos na lista "registros"
registros = carregar_dados("halloween_vendas.csv")
# confere se leu tudo: deve aparecer 1500
print("Total de registros:", len(registros))
# mostra os 3 primeiros pedidos
mostrar_primeiros(registros)
# vê todas as escritas diferentes da coluna categoria (antes da limpeza)
print("Categorias distintas:", valores_distintos(registros, "categoria"))
# padroniza a coluna categoria nos 1500 pedidos
vazias_preenchidas, nao_vazias_alteradas = padronizar_categorias(registros)
print("Categorias vazias preenchidas:", vazias_preenchidas)
print("Categorias não vazias alteradas:", nao_vazias_alteradas)
# mostra como ficou depois da limpeza
print("Categorias depois:", valores_distintos(registros, "categoria"))
# vê as escritas diferentes de canal_venda (antes da limpeza)
print("Canais antes:", valores_distintos(registros, "canal_venda"))
# padroniza a coluna canal_venda nos 1500 pedidos
canais_corrigidos, canais_nao_reconhecidos = padronizar_canais(registros)
print("Canais corrigidos:", canais_corrigidos)
print("Canais não reconhecidos:", canais_nao_reconhecidos)
# mostra como ficou depois da limpeza
print("Canais depois:", valores_distintos(registros, "canal_venda"))

def validar_numeros(registros):
    problemas_quantidade = 0
    problemas_preco = 0
    pedidos_afetados = 0
    for registro in registros:
        # lista de problemas deste pedido (começa vazia)
        problemas = []
        ok_q, resultado_q = validar_quantidade(registro["quantidade"])
        if not ok_q:
            problemas_quantidade += 1
            problemas.append("quantidade: " + resultado_q)
        ok_p, resultado_p = validar_preco(registro["preco_unitario"])
        if not ok_p:
            problemas_preco += 1
            problemas.append("preco_unitario: " + resultado_p)
        # marca no pedido, sem apagar nem inventar valor
        registro["problemas"] = problemas
        # conta o pedido uma única vez, mesmo com dois defeitos
        if problemas:
            pedidos_afetados += 1
    return problemas_quantidade, problemas_preco, pedidos_afetados
# valida quantidade e preço (só marca os problemas, não altera os valores)
problemas_quantidade, problemas_preco, pedidos_afetados = validar_numeros(registros)
print("Problemas em quantidade:", problemas_quantidade)
print("Problemas em preço:", problemas_preco)
print("Pedidos afetados:", pedidos_afetados)