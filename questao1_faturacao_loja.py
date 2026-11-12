
import heapq
import itertools
from datetime import datetime

LIMITE_BONUS = 100_000   # Kz
TAXA_BONUS = 0.10        # 10%
IDADE_IDOSO = 65

fila = []                      # heap: (prioridade, ordem_chegada, cliente)
ordem = itertools.count(1)
faturas = []                   # faturas já emitidas


def kz(valor):
    return f"{valor:,.2f} Kz".replace(",", " ")


def ler_texto(msg):
    while True:
        t = input(msg).strip()
        if t:
            return t
        print("  Campo obrigatório.")


def ler_sn(msg):
    while True:
        r = input(msg + " (s/n): ").strip().lower()
        if r in ("s", "n"):
            return r == "s"
        print("  Responda com 's' ou 'n'.")


def ler_int(msg, minimo=0, maximo=130):
    while True:
        try:
            v = int(input(msg))
            if minimo <= v <= maximo:
                return v
        except ValueError:
            pass
        print(f"  Introduza um número inteiro entre {minimo} e {maximo}.")


def ler_valor(msg):
    while True:
        try:
            v = float(input(msg).replace(" ", "").replace(",", "."))
            if v >= 0:
                return v
        except ValueError:
            pass
        print("  Introduza um valor numérico válido (>= 0).")


def ler_genero():
    while True:
        g = input("Género (M/F): ").strip().upper()
        if g in ("M", "F"):
            return g
        print("  Introduza M ou F.")


def motivos_prioridade(c):
    m = []
    if c["genero"] == "F" and c["gravida"]:
        m.append("Mulher grávida")
    if c["idade"] >= IDADE_IDOSO:
        m.append("Pessoa idosa")
    if c["deficiencia"]:
        m.append("Pessoa com deficiência")
    return m


def registar_cliente():
    print("\n--- Registo de Cliente ---")
    nome = ler_texto("Nome do cliente: ")
    genero = ler_genero()
    idade = ler_int("Idade: ")
    gravida = ler_sn("Está grávida?") if genero == "F" else False
    deficiencia = ler_sn("Tem alguma deficiência?")
    total = ler_valor("Valor total das compras (Kz): ")

    cliente = {
        "nome": nome, "genero": genero, "idade": idade,
        "gravida": gravida, "deficiencia": deficiencia,
        "total": total, "chegada": datetime.now().strftime("%H:%M:%S"),
    }
    cliente["motivos"] = motivos_prioridade(cliente)
    prioridade = 0 if cliente["motivos"] else 1
    senha = next(ordem)
    cliente["senha"] = senha
    heapq.heappush(fila, (prioridade, senha, cliente))

    print(f"\nCliente registado. Senha n.º {senha:03d} "
          f"({'PRIORITÁRIO: ' + ', '.join(cliente['motivos']) if prioridade == 0 else 'atendimento normal'}).")


def calcular_fatura(c):
    bruto = c["total"]
    tem_bonus = bruto > LIMITE_BONUS
    bonus = bruto * TAXA_BONUS if tem_bonus else 0.0
    return {"bruto": bruto, "bonus": bonus, "liquido": bruto - bonus, "tem_bonus": tem_bonus}


def atender_proximo():
    if not fila:
        print("\nNão há clientes na fila.")
        return
    _, _, c = heapq.heappop(fila)
    f = calcular_fatura(c)
    f.update(cliente=c["nome"], senha=c["senha"], data=datetime.now().strftime("%d/%m/%Y %H:%M"))
    faturas.append(f)

    print("\n" + "=" * 46)
    print(f"  FATURA n.º {len(faturas):04d}   {f['data']}")
    print("=" * 46)
    print(f"  Cliente : {c['nome']} (senha {c['senha']:03d})")
    if c["motivos"]:
        print(f"  Prioridade de atendimento: {', '.join(c['motivos'])}")
    print(f"  Total das compras : {kz(f['bruto'])}")
    if f["tem_bonus"]:
        print(f"  Bónus comercial 10%: -{kz(f['bonus'])}")
    else:
        print(f"  Bónus comercial    : não elegível (compras <= {kz(LIMITE_BONUS)})")
    print(f"  TOTAL A PAGAR     : {kz(f['liquido'])}")
    print("=" * 46)


def mostrar_fila():
    print("\n--- Fila de espera (ordem de atendimento) ---")
    if not fila:
        print("Fila vazia.")
        return
    for i, (p, _, c) in enumerate(sorted(fila), 1):
        tipo = "PRIORITÁRIO" if p == 0 else "Normal"
        extra = f" [{', '.join(c['motivos'])}]" if c["motivos"] else ""
        print(f"{i:2d}. Senha {c['senha']:03d} | {c['nome']} | {tipo}{extra} | chegada {c['chegada']}")


def resumo():
    print("\n--- Resumo do dia ---")
    print(f"Faturas emitidas: {len(faturas)}")
    print(f"Total faturado  : {kz(sum(f['liquido'] for f in faturas))}")
    print(f"Bónus atribuídos: {kz(sum(f['bonus'] for f in faturas))} "
          f"({sum(1 for f in faturas if f['tem_bonus'])} clientes)")


def menu():
    opcoes = {
        "1": ("Registar cliente / compras", registar_cliente),
        "2": ("Atender próximo cliente e emitir fatura", atender_proximo),
        "3": ("Ver fila de espera", mostrar_fila),
        "4": ("Resumo do dia", resumo),
    }
    while True:
        print("\n===== LOJA DE PRODUTOS ALIMENTARES =====")
        for k, (t, _) in opcoes.items():
            print(f" {k} - {t}")
        print(" 0 - Sair")
        op = input("Opção: ").strip()
        if op == "0":
            print("Até breve!")
            break
        if op in opcoes:
            opcoes[op][1]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
