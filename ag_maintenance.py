import random
from itertools import product

CAP = [20, 15, 35, 40, 15, 15, 10]
DEM = [80, 90, 65, 70]
TOTAL = sum(CAP)
N_UNITS, N_INT = len(CAP), len(DEM)

OPTIONS = [["1100", "0110", "0011"]] * 2 + [["1000", "0100", "0010", "0001"]] * 5
GROUPES = [(0, 1), (2, 6)]


def reserves(ch):
    res = []
    for t in range(N_INT):
        perdue = sum(CAP[u] for u in range(N_UNITS) if ch[u][t] == "1")
        res.append(TOTAL - perdue - DEM[t])
    return res


def fitness(ch):
    return max(0, min(reserves(ch)))


def individu_aleatoire():
    return [random.choice(OPTIONS[u]) for u in range(N_UNITS)]


def selection_loterie(pop, fits):
    total = sum(fits)
    if total == 0:
        return random.choice(pop)[:]
    r = random.uniform(0, total)
    cumul = 0
    for ind, f in zip(pop, fits):
        cumul += f
        if r <= cumul:
            return ind[:]
    return pop[-1][:]


def croisement(p1, p2):
    pt = random.randint(1, N_UNITS - 1)
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]


def mutation(ch, pm, type_mut="inversion"):
    ch = ch[:]
    if type_mut == "inversion_segment":
        if random.random() < pm:
            a, b = random.choice(GROUPES)
            i, j = sorted(random.sample(range(a, b + 1), 2))
            ch[i:j + 1] = ch[i:j + 1][::-1]
        return ch
    for u in range(N_UNITS):
        if random.random() < pm:
            if type_mut == "inversion":
                ch[u] = ch[u][::-1]
            else:
                ch[u] = random.choice(OPTIONS[u])
    return ch


def algo_genetique(taille_pop=50, generations=100, pc=0.8, pm=0.1,
                   type_mut="inversion", seed=None):
    if seed is not None:
        random.seed(seed)
    pop = [individu_aleatoire() for _ in range(taille_pop)]
    historique = []
    meilleur = max(pop, key=fitness)
    for g in range(generations):
        fits = [fitness(i) for i in pop]
        b = pop[fits.index(max(fits))]
        if fitness(b) > fitness(meilleur):
            meilleur = b[:]
        historique.append((max(fits), sum(fits) / len(fits)))
        nouvelle = [meilleur[:]]
        while len(nouvelle) < taille_pop:
            p1, p2 = selection_loterie(pop, fits), selection_loterie(pop, fits)
            if random.random() < pc:
                e1, e2 = croisement(p1, p2)
            else:
                e1, e2 = p1, p2
            nouvelle += [mutation(e1, pm, type_mut), mutation(e2, pm, type_mut)]
        pop = nouvelle[:taille_pop]
    return meilleur, historique


def force_brute():
    return max((list(c) for c in product(*OPTIONS)), key=fitness)


def afficher(ch):
    print("  Chromosome :", " ".join(ch))
    for t in range(N_INT):
        en_maint = [u + 1 for u in range(N_UNITS) if ch[u][t] == "1"]
        print(f"  Intervalle {t+1}: unités en maintenance {en_maint}, "
              f"réserve = {reserves(ch)[t]} MW")
    print("  Performance (plus petite réserve) =", fitness(ch))


if __name__ == "__main__":
    opt = force_brute()
    print("Optimum exact (force brute) :")
    afficher(opt)
    for tm in ("inversion", "inversion_segment", "aleatoire"):
        best, hist = algo_genetique(type_mut=tm, seed=1)
        print(f"\nAG - mutation '{tm}' :")
        afficher(best)
        gen_opt = next((i + 1 for i, (m, _) in enumerate(hist) if m >= fitness(opt)), None)
        print("  Optimum atteint à la génération :", gen_opt)

    try:
        import matplotlib.pyplot as plt
        _, hist = algo_genetique(type_mut="inversion", seed=1)
        plt.plot([h[0] for h in hist], label="Meilleure")
        plt.plot([h[1] for h in hist], label="Moyenne")
        plt.xlabel("Génération")
        plt.ylabel("Performance (MW)")
        plt.legend()
        plt.title("Convergence de l'AG")
        plt.savefig("convergence.png")
    except ImportError:
        pass