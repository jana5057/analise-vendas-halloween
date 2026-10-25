import csv

# CÓDIGO DO SPRINT 1 (Leitura do arquivo)
def carregar_dados(caminho):
    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        return list(leitor)


registros = carregar_dados("halloween_vendas.csv")
print("Total de registros:", len(registros))
for registro in registros[:3]:
    print(registro)
