# ============ IMPORTS ============
import csv  # 🔒 biblioteca do Python para ler arquivos .csv


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


# ============ EXECUÇÃO ============
# 📄 lê o arquivo e guarda os 1500 pedidos na lista "registros"
registros = carregar_dados("halloween_vendas.csv")
# confere se leu tudo: deve aparecer 1500
print("Total de registros:", len(registros))
# mostra os 3 primeiros pedidos
mostrar_primeiros(registros)