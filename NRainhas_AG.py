import random
import time

# *****************************
# Geração de tabuleiro com bloqueios aprimorado (7% a 13%)
# *****************************
def gerar_tabuleiro_com_bloqueios_melhorado(n, num_bloqueios=None, seed=None, percentual_max=0.13):
    if seed is not None:
        random.seed(seed)

    total_casas = n * n
    max_bloqueios = int(min(total_casas - n, percentual_max * total_casas))

    if num_bloqueios is None:
        num_bloqueios = int(0.07 * total_casas)
    elif num_bloqueios > max_bloqueios:
        raise ValueError(f"Número de bloqueios ({num_bloqueios}) excede o máximo permitido ({max_bloqueios}) para n={n}.")

    tabuleiro = [['.' for _ in range(n)] for _ in range(n)]
    bloqueios = set()

    while len(bloqueios) < num_bloqueios:
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        if (i, j) not in bloqueios:
            tabuleiro[i][j] = 'X'
            bloqueios.add((i, j))

    return tabuleiro, bloqueios

# *****************************
# Funções para o Algoritmo Genético com Elitismo e Minirepair
# *****************************

def inicializar_populacao(n, bloqueios, tam_pop, seed=None):
    if seed is not None:
        random.seed(seed)
    populacao = []
    for _ in range(tam_pop):
        individuo = [random.choice([c for c in range(n) if (linha, c) not in bloqueios])
                    for linha in range(n)]
        populacao.append(individuo)
    return populacao


def conflitos(individuo):
    n = len(individuo)
    cont = 0
    for i in range(n):
        for j in range(i+1, n):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                cont += 1
    return cont


def fitness(individuo):
    n = len(individuo)
    total_pares = n * (n - 1) // 2
    return total_pares - conflitos(individuo)


def minirepair(individuo, bloqueios, max_iters=5):
    for _ in range(max_iters):
        conflicts = [(i, individuo[i]) for i in range(len(individuo)) if any(
            individuo[i] == individuo[j] or abs(individuo[i]-individuo[j]) == abs(i-j)
            for j in range(len(individuo)) if j != i)]
        if not conflicts:
            break
        i, _ = random.choice(conflicts)
        # tenta melhor coluna sem bloqueio que minimize conflitos na linha i
        best_col, best_fit = individuo[i], -1
        for c in range(len(individuo)):
            if (i, c) in bloqueios: continue
            temp = individuo[:]
            temp[i] = c
            f = fitness(temp)
            if f > best_fit:
                best_fit, best_col = f, c
        individuo[i] = best_col
    return individuo


def tournament_selection(pop, fit_vals, k=3):
    competidores = random.sample(range(len(pop)), k)
    vencedor = max(competidores, key=lambda i: fit_vals[i])
    return pop[vencedor]


def crossover(pai1, pai2, pc):
    n = len(pai1)
    if random.random() < pc:
        ponto = random.randint(1, n-1)
        return pai1[:ponto] + pai2[ponto:], pai2[:ponto] + pai1[ponto:]
    return pai1[:], pai2[:]


def mutacao(individuo, bloqueios, pm):
    n = len(individuo)
    for i in range(n):
        if random.random() < pm:
            individuo[i] = random.choice([c for c in range(n) if (i, c) not in bloqueios])
    return individuo


def algoritmo_genetico(n, bloqueios, tam_pop=100, geracoes=2000, pc=0.8, pm=0.2,elitismo_k=5, seed=None):
    pop = inicializar_populacao(n, bloqueios, tam_pop, seed)
    melhor_sol, melhor_fit = None, -1
    historico = []

    for g in range(1, geracoes+1):
        fit_vals = [fitness(ind) for ind in pop]
        max_f, avg_f = max(fit_vals), sum(fit_vals)/len(fit_vals)
        historico.append((g, max_f, avg_f))
        # Atualiza melhor solução global
        if max_f > melhor_fit:
            melhor_fit = max_f
            melhor_sol = pop[fit_vals.index(max_f)][:]
        # Condição de parada
        if melhor_fit == n*(n-1)//2:
            break
        # Ordena por fitness decrescente para elitismo
        pop_sorted = [ind for _, ind in sorted(zip(fit_vals, pop), key=lambda x: x[0], reverse=True)]
        nova_pop = pop_sorted[:elitismo_k]  # preserva elites
        while len(nova_pop) < tam_pop:
            p1 = tournament_selection(pop, fit_vals)
            p2 = tournament_selection(pop, fit_vals)
            f1, f2 = crossover(p1, p2, pc)
            f1 = minirepair(f1, bloqueios)
            f2 = minirepair(f2, bloqueios)
            nova_pop.append(mutacao(f1, bloqueios, pm))
            if len(nova_pop) < tam_pop:
                nova_pop.append(mutacao(f2, bloqueios, pm))
        pop = nova_pop

    return melhor_sol, historico

# *****************************
# Testes para diferentes tamanhos
# *****************************
def main():
    testes = [1,2,5,8,9,10,12,16,20] 
    resultados = []
    for n in testes:
        tab, bloqueios = gerar_tabuleiro_com_bloqueios_melhorado(n, seed=42)
        start = time.time()
        sol, hist = algoritmo_genetico(n, bloqueios, tam_pop=200, geracoes=2000, seed=42)
        tempo = (time.time() - start) * 1000  # ms
        sucesso = sol is not None and fitness(sol) == n*(n-1)//2
        gens = hist[-1][0]
        resultados.append((n, sucesso, gens, f"{tempo:.2f} ms"))
        print(f"n={n} | Solução: {sucesso} | Gerações: {gens} | Tempo: {tempo:.2f} ms")
    print("\nTabela de resultados:")
    print("n | Solução Encontrada | Gerações Usadas | Tempo")
    for r in resultados:
        print(f"{r[0]:>3} | {str(r[1]):^17} | {r[2]:>14} | {r[3]:>10}")

# *****************************
# Testes com até 1000 execuções
# *****************************
def testar_limite_n():
    testes = [8, 12, 16, 20,]  
    max_execucoes = 1000
    for n in testes:
        sucesso_count = 0
        for execucao in range(max_execucoes):
            tab, bloqueios = gerar_tabuleiro_com_bloqueios_melhorado(n, seed=42 + execucao)
            sol, hist = algoritmo_genetico(n, bloqueios, tam_pop=200, geracoes=2000, seed=42 + execucao)
            if sol is not None and fitness(sol) == n*(n-1)//2:
                sucesso_count += 1
        print(f"n={n} | Sucesso em {sucesso_count}/{max_execucoes} execuções")

# *****************************
# Seleção de modo de execução
# *****************************
if __name__ == '__main__':
    modo = input("Digite '1' para testes padrão ou '2' para testar limite de n (1000 execuções): ")
    if modo == '2':
        testar_limite_n()
    else:
        main()

