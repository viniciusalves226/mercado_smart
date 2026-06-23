"""
Mercado Smart - Versão com estoque, cadastro e reposição
"""

from datetime import datetime
import json
import os

ARQUIVO_DADOS = "mercado_dados.json"

produtos_catalogo = [
    {"id": 1, "nome": "Arroz Tipo 1 5kg", "marca": "Camil", "categoria": "Alimentos", "preco": 22.90, "estoque": 45},
    {"id": 2, "nome": "Feijão Carioca 1kg", "marca": "Camil", "categoria": "Alimentos", "preco": 8.50, "estoque": 38},
]

caixa = {
    "saldo_inicial": 500.0,
    "entradas": [],
    "saidas": [],
    "vendas": []
}

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump({"produtos": produtos_catalogo, "caixa": caixa}, f, ensure_ascii=False, indent=4)

def carregar_dados():
    global produtos_catalogo, caixa

    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        produtos_catalogo = dados.get("produtos", produtos_catalogo)
        caixa = dados.get("caixa", caixa)

def fmt_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def buscar_produto(pid):
    return next((p for p in produtos_catalogo if p["id"] == pid), None)

def listar_produtos():
    print("\n=== PRODUTOS CADASTRADOS ===")

    if not produtos_catalogo:
        print("Nenhum produto cadastrado.")
        return

    for p in produtos_catalogo:
        print(
            f"ID: {p['id']} | {p['nome']} | "
            f"Preço: {fmt_brl(p['preco'])} | Estoque: {p['estoque']}"
        )

def adicionar_produto():
    produtos_adicionados = 0

    while True:
        try:
            novo_id = max([p["id"] for p in produtos_catalogo], default=0) + 1

            print(f"\n--- Novo produto (ID {novo_id}) ---")
            nome = input("Nome do produto: ")
            marca = input("Marca: ")
            categoria = input("Categoria: ")
            preco = float(input("Preço: ").replace(",", "."))
            estoque = int(input("Estoque inicial: "))

            produtos_catalogo.append({
                "id": novo_id,
                "nome": nome,
                "marca": marca,
                "categoria": categoria,
                "preco": preco,
                "estoque": estoque
            })

            produtos_adicionados += 1
            print(f"✓ Produto '{nome}' adicionado com sucesso!")

        except ValueError:
            print("Dados inválidos. Esse produto não foi adicionado.")

        continuar = input("\nAdicionar outro produto? (s/n): ").strip().lower()
        if continuar != "s":
            break

    if produtos_adicionados > 0:
        salvar_dados()
        print(f"\n✓ {produtos_adicionados} produto(s) adicionado(s) e salvo(s) com sucesso!")
    else:
        print("\nNenhum produto foi adicionado.")

def remover_produto():
    try:
        listar_produtos()

        pid = int(input("\nID do produto para remover: "))
        produto = buscar_produto(pid)

        if not produto:
            print("Produto não encontrado.")
            return

        produtos_catalogo.remove(produto)
        salvar_dados()

        print(f"✓ Produto '{produto['nome']}' removido.")

    except ValueError:
        print("ID inválido.")

def repor_estoque():
    try:
        listar_produtos()

        pid = int(input("\nID do produto: "))
        produto = buscar_produto(pid)

        if not produto:
            print("Produto não encontrado.")
            return

        qtd = int(input("Quantidade a adicionar: "))

        if qtd <= 0:
            print("Quantidade inválida.")
            return

        produto["estoque"] += qtd

        salvar_dados()

        print(f"✓ Estoque atualizado! Agora possui {produto['estoque']} unidades.")

    except ValueError:
        print("Valor inválido.")

def registrar_venda():
    try:
        listar_produtos()

        pid = int(input("\nID do produto: "))
        produto = buscar_produto(pid)

        if not produto:
            print("Produto não encontrado.")
            return

        qtd = int(input("Quantidade: "))

        if qtd <= 0 or qtd > produto["estoque"]:
            print("Quantidade inválida.")
            return

        total = qtd * produto["preco"]
        produto["estoque"] -= qtd

        caixa["vendas"].append({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "produto": produto["nome"],
            "qtd": qtd,
            "total": total
        })

        caixa["entradas"].append({
            "descricao": "Venda",
            "valor": total
        })

        salvar_dados()

        print(f"Venda registrada: {fmt_brl(total)}")

    except ValueError:
        print("Entrada inválida.")

def relatorio():
    print("\n=== RELATÓRIO ===")

    total = sum(v["total"] for v in caixa["vendas"])

    print(f"Total de vendas: {len(caixa['vendas'])}")
    print(f"Faturamento: {fmt_brl(total)}")

    print("\n=== ÚLTIMAS VENDAS ===")

    for venda in caixa["vendas"][-10:]:
        print(
            f"{venda['data']} | {venda['produto']} | "
            f"{venda['qtd']} un | {fmt_brl(venda['total'])}"
        )

def menu():
    carregar_dados()

    while True:
        print("\n=== MERCADO SMART ===")
        print("1 - Registrar venda")
        print("2 - Relatório")
        print("3 - Listar produtos")
        print("4 - Adicionar produto")
        print("5 - Remover produto")
        print("6 - Repor estoque")
        print("0 - Sair")

        op = input("Opção: ")

        if op == "1":
            registrar_venda()
        elif op == "2":
            relatorio()
        elif op == "3":
            listar_produtos()
        elif op == "4":
            adicionar_produto()
        elif op == "5":
            remover_produto()
        elif op == "6":
            repor_estoque()
        elif op == "0":
            salvar_dados()
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()