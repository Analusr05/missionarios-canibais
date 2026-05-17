import time
from collections import deque

class util:

    class Queue:
        def __init__(self):
            self._dados = deque()

        def push(self, item):
            self._dados.append(item)

        def pop(self):
            return self._dados.popleft()

        def isEmpty(self):
            return len(self._dados) == 0

    class Stack:
        def __init__(self):
            self._dados = []

        def push(self, item):
            self._dados.append(item)

        def pop(self):
            return self._dados.pop()

        def isEmpty(self):
            return len(self._dados) == 0

class search_tree:

    @staticmethod
    def getStartNode(problema):
        return {
            "STATE" : problema.getStartState(),
            "PARENT": None,
            "ACTION": None,
            "DEPTH" : 0,
        }

    @staticmethod
    def getChildNode(sucessor, pai):
        novo_estado, acao = sucessor
        return {
            "STATE" : novo_estado,
            "PARENT": pai,
            "ACTION": acao,
            "DEPTH" : pai["DEPTH"] + 1,
        }

    @staticmethod
    def getActionSequence(node):
        acoes = []
        atual = node
        while atual["PARENT"] is not None:
            acoes.append(atual["ACTION"])
            atual = atual["PARENT"]
        return list(reversed(acoes))

    @staticmethod
    def getNodeSequence(node):
        nos = []
        atual = node
        while atual is not None:
            nos.append(atual)
            atual = atual["PARENT"]
        return list(reversed(nos))

TOTAL          = 3
ESTADO_INICIAL = (3, 3, 0)
ESTADO_FINAL   = (0, 0, 1)

ACOES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
DESCRICAO_ACAO = {
    (1, 0): "1 missionário",
    (2, 0): "2 missionários",
    (0, 1): "1 canibal",
    (0, 2): "2 canibais",
    (1, 1): "1 missionário + 1 canibal",
}

class Problema:

    def getStartState(self):
        return ESTADO_INICIAL

    def isGoalState(self, estado):
        return estado == ESTADO_FINAL

    def expand(self, estado):
        m_esq, c_esq, barco = estado
        filhos = []

        for (mb, cb) in ACOES:
            if barco == 0:
                novo_m = m_esq - mb
                novo_c = c_esq - cb
            else:
                novo_m = m_esq + mb
                novo_c = c_esq + cb

            novo_estado = (novo_m, novo_c, 1 - barco)

            if self._eh_valido(novo_m, novo_c):
                filhos.append((novo_estado, (mb, cb)))

        return filhos

    def _eh_valido(self, m_esq, c_esq):
        m_dir = TOTAL - m_esq
        c_dir = TOTAL - c_esq

        if not (0 <= m_esq <= TOTAL and 0 <= c_esq <= TOTAL):
            return False
        if not (0 <= m_dir <= TOTAL and 0 <= c_dir <= TOTAL):
            return False
        if m_esq > 0 and c_esq > m_esq:
            return False
        if m_dir > 0 and c_dir > m_dir:
            return False

        return True

def breadthFirstSearch(problema):
    node = search_tree.getStartNode(problema)

    frontier = util.Queue()
    frontier.push(node)
    explored = set()

    gerados  = 1
    visitados = 0

    while not frontier.isEmpty():
        node = frontier.pop()

        if node["STATE"] in explored:
            continue

        explored.add(node["STATE"])
        visitados += 1

        if problema.isGoalState(node["STATE"]):
            return search_tree.getActionSequence(node), \
                   search_tree.getNodeSequence(node), \
                   gerados, visitados, node["DEPTH"]

        for sucessor in problema.expand(node["STATE"]):
            child_node = search_tree.getChildNode(sucessor, node)
            gerados += 1
            frontier.push(child_node)

    return [], [], gerados, visitados, -1


def depthFirstSearch(problema, limite=50):
    node = search_tree.getStartNode(problema)

    frontier = util.Stack()
    frontier.push(node)
    explored = set()

    gerados  = 1
    visitados = 0

    while not frontier.isEmpty():
        node = frontier.pop()

        if node["STATE"] in explored:
            continue

        explored.add(node["STATE"])
        visitados += 1

        if problema.isGoalState(node["STATE"]):
            return search_tree.getActionSequence(node), \
                   search_tree.getNodeSequence(node), \
                   gerados, visitados, node["DEPTH"]

        if node["DEPTH"] < limite:
            for sucessor in reversed(problema.expand(node["STATE"])):
                child_node = search_tree.getChildNode(sucessor, node)
                gerados += 1
                frontier.push(child_node)

    return [], [], gerados, visitados, -1


def _depthLimitedSearch(node, problema, limite, explored, cont):
    cont["gerados"] += 1

    if node["STATE"] in explored:
        return None

    if problema.isGoalState(node["STATE"]):
        cont["visitados"] += 1
        return node

    if node["DEPTH"] >= limite:
        return None

    explored.add(node["STATE"])
    cont["visitados"] += 1

    for sucessor in problema.expand(node["STATE"]):
        child_node = search_tree.getChildNode(sucessor, node)
        resultado  = _depthLimitedSearch(child_node, problema, limite, explored, cont)
        if resultado is not None:
            return resultado

    explored.discard(node["STATE"])
    return None


def iterativeDeepeningSearch(problema, max_prof=50):
    total_g = 0
    total_v = 0

    for limite in range(max_prof + 1):
        node = search_tree.getStartNode(problema)
        cont = {"gerados": 0, "visitados": 0}

        resultado = _depthLimitedSearch(node, problema, limite, set(), cont)
        total_g  += cont["gerados"]
        total_v  += cont["visitados"]

        if resultado is not None:
            return search_tree.getActionSequence(resultado), \
                   search_tree.getNodeSequence(resultado), \
                   total_g, total_v, resultado["DEPTH"]

    return [], [], total_g, total_v, -1

def descrever_estado(estado):
    m_esq, c_esq, barco = estado
    m_dir = TOTAL - m_esq
    c_dir = TOTAL - c_esq
    lado  = "ESQ" if barco == 0 else "DIR"
    return f"Esq:[{m_esq}M {c_esq}C]  Barco:{lado}  Dir:[{m_dir}M {c_dir}C]"


def imprimir_caminho(nos):
    print(f"\n  {'PASSO':<6} {'AÇÃO':<32} {'ESTADO'}")
    print("  " + "─" * 72)
    for i, no in enumerate(nos):
        if no["ACTION"] is None:
            acao_str = "Estado inicial"
        else:
            mb, cb   = no["ACTION"]
            direcao  = "→ DIR" if no["STATE"][2] == 1 else "← ESQ"
            acao_str = f"{direcao}  {DESCRICAO_ACAO[(mb, cb)]}"
        print(f"  {i:<6} {acao_str:<32} {descrever_estado(no['STATE'])}")


def imprimir_arvore(nos):
    print(f"\n  {'PROF':<6} {'ESTADO'}")
    print("  " + "─" * 60)
    for no in nos:
        prof   = no["DEPTH"]
        indent = "    " * prof
        conect = "└── " if prof > 0 else ""
        print(f"  {prof:<6} {indent}{conect}{descrever_estado(no['STATE'])}")


def executar_algoritmo(nome, func, problema):
    sep = "═" * 72
    print(f"\n{sep}")
    print(f"  {nome}")
    print(sep)

    inicio = time.perf_counter()
    acoes, nos, gerados, visitados, passos = func(problema)
    tempo  = time.perf_counter() - inicio

    if acoes is not None and passos >= 0:
        print(f"\n   Solução encontrada em {passos} passos")
        print(f"     Estados gerados   : {gerados}")
        print(f"     Estados visitados : {visitados}")
        print(f"     Tempo             : {tempo * 1000:.4f} ms")

        print("\n  ── Caminho da solução ──")
        imprimir_caminho(nos)

        print("\n  ── Árvore de busca (caminho da solução) ──")
        imprimir_arvore(nos)
    else:
        print("Nenhuma solução encontrada.")

    return {
        "nome"     : nome,
        "passos"   : passos,
        "gerados"  : gerados,
        "visitados": visitados,
        "tempo_ms" : round(tempo * 1000, 4),
    }

def main():
    problema = Problema()

    print(f"\n  Estado inicial : {descrever_estado(problema.getStartState())}")
    print(f"  Estado final   : {descrever_estado(ESTADO_FINAL)}")

    resultados = [
        executar_algoritmo("BFS   — Busca em Largura",         breadthFirstSearch, problema),
        executar_algoritmo("DFS   — Busca em Profundidade",    depthFirstSearch,   problema),
        executar_algoritmo("IDDFS — Aprofundamento Iterativo", iterativeDeepeningSearch, problema),
    ]

    sep = "═" * 72
    print(f"\n{sep}")
    print("  COMPARAÇÃO DOS ALGORITMOS")
    print(sep)
    print(f"\n  {'Algoritmo':<38} {'Passos':>6} {'Gerados':>8} {'Visitados':>10} {'Tempo(ms)':>11}")
    print("  " + "─" * 68)
    for r in resultados:
        print(f"  {r['nome']:<38} {r['passos']:>6} {r['gerados']:>8} "
              f"{r['visitados']:>10} {r['tempo_ms']:>11.4f}")
    print()


if __name__ == "__main__":
    main()
