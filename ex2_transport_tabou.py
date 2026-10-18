from collections import deque
import itertools


couts    = [[5, 3, 4],
            [6, 7, 2]]
offres   = [8, 9]
demandes = [4, 5, 8]
NB_D, NB_M = len(offres), len(demandes)


def cout_total(x):
    return sum(couts[i][j] * x[i][j] for i in range(NB_D) for j in range(NB_M))


def est_realisable(x):
    if any(x[i][j] < 0 for i in range(NB_D) for j in range(NB_M)):
        return False
    if any(sum(x[i]) != offres[i] for i in range(NB_D)):
        return False
    return all(sum(x[i][j] for i in range(NB_D)) == demandes[j] for j in range(NB_M))


def solution_initiale_coin_nord_ouest():
    x = [[0] * NB_M for _ in range(NB_D)]
    o, d = offres[:], demandes[:]
    i = j = 0
    while i < NB_D and j < NB_M:
        q = min(o[i], d[j])
        x[i][j] = q
        o[i] -= q
        d[j] -= q
        if o[i] == 0:
            i += 1
        else:
            j += 1
    return x


def solution_initiale_gloutonne():
    x = [[0] * NB_M for _ in range(NB_D)]
    o, d = offres[:], demandes[:]
    cases = sorted(((couts[i][j], i, j) for i in range(NB_D) for j in range(NB_M)))
    for _, i, j in cases:
        q = min(o[i], d[j])
        x[i][j] = q
        o[i] -= q
        d[j] -= q
    return x


def voisins(x):
    base = cout_total(x)
    for i1, i2 in itertools.permutations(range(NB_D), 2):
        for j1, j2 in itertools.permutations(range(NB_M), 2):
            if x[i1][j2] >= 1 and x[i2][j1] >= 1:
                y = [ligne[:] for ligne in x]
                y[i1][j1] += 1
                y[i1][j2] -= 1
                y[i2][j1] -= 1
                y[i2][j2] += 1
                delta = couts[i1][j1] - couts[i1][j2] - couts[i2][j1] + couts[i2][j2]
                yield (i1, i2, j1, j2), y, base + delta


def cle(mv):
    i1, i2, j1, j2 = mv
    return frozenset({(i1, j1), (i2, j2)})


def recherche_tabou(x0, longueur_tabou=4, max_iter=6, verbose=True):
    x = [l[:] for l in x0]
    best, best_cout = [l[:] for l in x], cout_total(x)
    tabou = deque(maxlen=longueur_tabou)

    if verbose:
        print(f"Solution initiale : {x}  ->  Z = {best_cout}")
        print("-" * 78)

    for k in range(1, max_iter + 1):
        meilleur_mv, meilleur_y, meilleur_c = None, None, None
        for mv, y, c in voisins(x):
            interdit = cle(mv) in tabou
            aspiration = c < best_cout
            if interdit and not aspiration:
                continue
            if meilleur_c is None or c < meilleur_c:
                meilleur_mv, meilleur_y, meilleur_c = mv, y, c

        if meilleur_mv is None:
            if verbose:
                print(f"Itération {k} : aucun voisin non tabou -> arrêt")
            break

        i1, i2, j1, j2 = meilleur_mv
        x = meilleur_y
        tabou.append(cle((i1, i2, j2, j1)))

        if meilleur_c < best_cout:
            best, best_cout = [l[:] for l in x], meilleur_c

        if verbose:
            print(f"Itération {k:2d} | mouvement D{i1+1}->M{j1+1}(+1) D{i2+1}->M{j2+1}(+1) "
                  f"| Z = {meilleur_c:3d} | meilleur Z = {best_cout:3d}")
            print(f"              x = {x}")
            print(f"              liste tabou = {[sorted((f'D{a+1}M{b+1}') for a, b in c) for c in tabou]}")
    return best, best_cout


def optimum_exact():
    meilleur, best_c = None, float("inf")
    for a in itertools.product(*[range(d + 1) for d in demandes]):
        if sum(a) != offres[0]:
            continue
        b = [demandes[j] - a[j] for j in range(NB_M)]
        x = [list(a), b]
        if est_realisable(x) and cout_total(x) < best_c:
            meilleur, best_c = x, cout_total(x)
    return meilleur, best_c


if __name__ == "__main__":
    assert sum(offres) == sum(demandes), "Problème non équilibré"

    print("=== 1) Départ : coin nord-ouest ===")
    x0 = solution_initiale_coin_nord_ouest()
    assert est_realisable(x0)
    sol, z = recherche_tabou(x0)
    print("\n>>> Meilleure solution Tabou :")
    for i in range(NB_D):
        print(f"    D{i+1} -> " + ", ".join(f"M{j+1}: {sol[i][j]}" for j in range(NB_M)))
    print(f"    Coût total minimal trouvé = {z}")

    print("\n=== 2) Départ : solution gloutonne ===")
    xg = solution_initiale_gloutonne()
    print(f"Glouton : {xg} -> Z = {cout_total(xg)}")
    sol_g, z_g = recherche_tabou(xg, verbose=False)
    print(f"Tabou depuis le glouton : Z = {z_g}")

    print("\n=== 3) Vérification par énumération exhaustive ===")
    opt, z_opt = optimum_exact()
    print(f"Optimum exact : {opt} -> Z = {z_opt}")
    print("Tabou a trouvé l'optimum." if z == z_opt else "Tabou n'a pas atteint l'optimum.")