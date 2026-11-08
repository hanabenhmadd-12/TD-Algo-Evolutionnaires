# Ordonnancement de la maintenance de centrales par Algorithme Génétique

## Problème

7 unités de production doivent être mises en maintenance pendant l'année, divisée en 4 intervalles. Le but est de maximiser la puissance en réserve.

| Unité | Capacité (MW) | Intervalles de maintenance requis |
|-------|---------------|-----------------------------------|
| 1     | 20            | 2                                 |
| 2     | 15            | 2                                 |
| 3     | 35            | 1                                 |
| 4     | 40            | 1                                 |
| 5     | 15            | 1                                 |
| 6     | 15            | 1                                 |
| 7     | 10            | 1                                 |

Capacité totale : 150 MW. Demande par intervalle : 80, 90, 65 et 70 MW.

## Formulation

**Variables de décision** : x[u][t] = 1 si l'unité u est en maintenance à l'intervalle t, 0 sinon.

**Encodage** : un chromosome est composé de 7 gènes de 4 bits (un gène par unité).

- Unités 1 et 2 : `1100`, `0110`, `0011` (2 intervalles consécutifs)
- Unités 3 à 7 : `1000`, `0100`, `0010`, `0001` (1 intervalle)

L'espace de recherche contient 3 × 3 × 4^5 = 9216 cédules.

**Puissance perdue** à l'intervalle t : P_t = Σ_u x[u][t] · C_u

**Réserve** à l'intervalle t : R_t = C_total − P_t − D_t

**Fonction objective (à maximiser)** :

f(chromosome) = max(0, min_t R_t)

**Contrainte** : R_t ≥ 0 pour tout t. Si une réserve est négative, la performance est ramenée à 0.

## Opérateurs génétiques

- **Sélection par loterie (roulette)** : probabilité de sélection P(i) = f_i / Σ f.
- **Croisement** : à 1 point, uniquement aux frontières des blocs de 4 bits.
- **Mutation par inversion** (toutes les variantes préservent la validité) :
  - `inversion` : inversion de l'ordre des 4 bits d'un gène (1100 ↔ 0011, 1000 ↔ 0001).
  - `inversion_segment` : inversion d'un segment de gènes au sein d'un groupe d'unités équivalentes ({1,2} ou {3 à 7}).
  - `aleatoire` : remplacement d'un gène par une valeur valide au hasard.
- **Élitisme** : le meilleur individu est conservé à chaque génération.

Paramètres : population = 50, générations = 100, pc = 0.8, pm = 0.1.

## Résultats

La recherche exhaustive donne une réserve minimale optimale de **25 MW**. L'AG atteint cet optimum avec les trois types de mutation.

## Exécution

```
python ag_maintenance.py
```
