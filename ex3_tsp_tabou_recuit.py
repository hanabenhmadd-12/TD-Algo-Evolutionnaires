import math
import random
import itertools
from collections import deque


PENALITE = 1000
ARETES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}
N = 8
INITIALE = [1, 2, 3, 4, 5, 6, 7, 8]


def dist(a, b):
    return ARETES.get((a, b), ARETES.get((b, a), PENALITE))


def cout(t):
    return sum(dist(t[i], t[(i + 1) % len(t)]) for i in range(len(t)))


def realisable(t):
    return cout(t) < PENALITE


def fmt(t):
    return "-".join(map(str, t + [t[0]]))


def deux_opt(t, p, q):
    return t[:p] + t[p:q + 1][::-1] + t[q + 1:]


def tous_les_voisins_positions():
    return [(p, q) for p, q in itertools.combinations(range(1, N), 2) if (p, q) != (1, N - 1)]


def tirer_voisin(rnd):
    return rnd.choice(tous_les_voisins_positions())


def tabou(depart, longueur_tabou=3, max_iter=10):
    s = depart[:]
    best, best_c = s[:], cout(s)
    liste = deque(maxlen=longueur_tabou)
    print(f"Solution initiale : {fmt(s)}   coût = {best_c}")
    print("-" * 86)
    print(f"{'k':>2} | {'mouvement':^13} | {'meilleur voisin non tabou':^27} | {'coût':^5} | {'best':^5} | liste tabou")
    for k in range(1, max_iter + 1):
        choix = None
        for p, q in tous_les_voisins_positions():
            v = deux_opt(s, p, q)
            c = cout(v)
            mv = frozenset((s[p], s[q]))
            if mv in liste and c >= best_c:
                continue
            if choix is None or c < choix[0]:
                choix = (c, v, mv)
        c, s, mv = choix
        liste.append(mv)
        if c < best_c:
            best, best_c = s[:], c
        paires = [tuple(sorted(m)) for m in liste]
        print(f"{k:>2} | 2-opt {str(tuple(sorted(mv))):<7}| {fmt(s):^27} | {c:^5} | {best_c:^5} | {paires}")
    return best, best_c


def recuit(depart, temperatures=(30, 20, 12, 7, 4), graine=10):
    rnd = random.Random(graine)
    s = depart[:]
    best, best_c = s[:], cout(s)
    print(f"Solution initiale : {fmt(s)}   coût = {best_c}")
    print("-" * 100)
    print(f"{'k':>2} | {'T':>3} | {'voisin (2-opt)':^18} | {'f(voisin)':^9} | {'delta':^6} | {'p':^6} | {'r':^6} | décision")
    for k, T in enumerate(temperatures, start=1):
        p_, q_ = tirer_voisin(rnd)
        v = deux_opt(s, p_, q_)
        delta = cout(v) - cout(s)
        if delta <= 0:
            p, r, ok = 1.0, float("nan"), True
        else:
            p = math.exp(-delta / T)
            r = rnd.random()
            ok = p > r
        print(f"{k:>2} | {T:>3} | {fmt(v):^18} | {cout(v):^9} | {delta:^6} | {p:^6.3f} | "
              f"{('-' if delta <= 0 else f'{r:.3f}'):^6} | {'accepté' if ok else 'rejeté'}")
        if ok:
            s = v
            if cout(s) < best_c:
                best, best_c = s[:], cout(s)
    print(f"\nSolution courante à la fin des 5 itérations : {fmt(s)}  coût = {cout(s)}")
    return best, best_c


def recuit_long(depart, T0=50.0, alpha=0.95, palier=50, T_min=0.1, graine=1):
    rnd = random.Random(graine)
    s = depart[:]
    best, best_c = s[:], cout(s)
    T = T0
    while T > T_min:
        for _ in range(palier):
            p_, q_ = tirer_voisin(rnd)
            v = deux_opt(s, p_, q_)
            delta = cout(v) - cout(s)
            if delta <= 0 or rnd.random() < math.exp(-delta / T):
                s = v
                if cout(s) < best_c:
                    best, best_c = s[:], cout(s)
        T *= alpha
    return best, best_c


def optimum_exact():
    meilleur, bc = None, float("inf")
    for perm in itertools.permutations(range(2, N + 1)):
        t = [1] + list(perm)
        c = cout(t)
        if c < bc:
            meilleur, bc = t, c
    return meilleur, bc


if __name__ == "__main__":
    print("=" * 86)
    print("RECHERCHE TABOU")
    print("=" * 86)
    bt, ct = tabou(INITIALE)
    print(f"\n>>> Meilleure tournée (Tabou) : {fmt(bt)}  coût = {ct}")

    print("\n" + "=" * 86)
    print("RECUIT SIMULÉ (5 itérations)")
    print("=" * 86)
    br, cr = recuit(INITIALE)
    print(f"\n>>> Meilleure tournée (Recuit, 5 it.) : {fmt(br)}  coût = {cr}")

    print("\n" + "=" * 86)
    print("COMPLÉMENTS")
    print("=" * 86)
    bl, cl = recuit_long(INITIALE)
    print(f"Recuit simulé long (T0=50, alpha=0.95) : {fmt(bl)}  coût = {cl}")
    be, ce = optimum_exact()
    print(f"Optimum exact (énumération 7! = 5040)   : {fmt(be)}  coût = {ce}")