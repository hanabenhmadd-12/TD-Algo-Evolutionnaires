import random
random.seed(42)
capacites = [20, 15, 35, 40, 15, 15, 10]
demandes = [80, 90, 65, 70]
capacite_totale = 150
possibles = [
    ["1100", "0110", "0011"],
    ["1100", "0110", "0011"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
]
taille_population = 50
nb_generations = 100
proba_croisement = 0.8
proba_mutation = 0.3
def calculer_reserves(chromosome):
    reserves = []
    for t in range(4):
        puissance_perdue = 0
        for u in range(7):
            if chromosome[u][t] == "1":
                puissance_perdue = puissance_perdue + capacites[u]
        reserve = capacite_totale - puissance_perdue - demandes[t]
        reserves.append(reserve)
    return reservesc
def fitness(chromosome):
    reserves = calculer_reserves(chromosome)
    plus_petite = min(reserves)
    if plus_petite < 0:
        return 0
    return plus_petite
def creer_chromosome():
    chromosome = []
    for options in possibles:
        chromosome.append(random.choice(options))
    return chromosome
def selection_loterie(population, scores):
    total = sum(scores)
    if total == 0:
        return random.choice(population)
    tirage = random.uniform(0, total)
    cumul = 0
    for i in range(len(population)):
        cumul = cumul + scores[i]
        if cumul >= tirage:
            return population[i]
    return population[-1]
def croisement(parent1, parent2):
    point = random.randint(1, 6)
    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]
    return enfant1, enfant2
def mutation_inversion(chromosome):
    chromosome = chromosome[:]
    if random.random() < 0.5:
        debut = 0
        fin = 1
    else:
        debut = 2
        fin = 6
    i, j = random.sample(range(debut, fin + 1), 2)
    if i > j:
        i, j = j, i
    partie = chromosome[i:j + 1]
    partie.reverse()
    chromosome[i:j + 1] = partie
    return chromosome
population = []
for _ in range(taille_population):
    population.append(creer_chromosome())

meilleur = population[0]

for generation in range(nb_generations):
    scores = []
    for chromosome in population:
        scores.append(fitness(chromosome))

    for i in range(taille_population):
        if scores[i] > fitness(meilleur):
            meilleur = population[i][:]

    if generation % 10 == 0:
        print("Génération", generation, ": meilleure fitness =", fitness(meilleur))
    nouvelle_population = [meilleur[:]]
    while len(nouvelle_population) < taille_population:

        parent1 = selection_loterie(population, scores)
        parent2 = selection_loterie(population, scores)
        if random.random() < proba_croisement:
            enfant1, enfant2 = croisement(parent1, parent2)
        else:
            enfant1 = parent1[:]
            enfant2 = parent2[:]
        if random.random() < proba_mutation:
            enfant1 = mutation_inversion(enfant1)
        if random.random() < proba_mutation:
            enfant2 = mutation_inversion(enfant2)

        nouvelle_population.append(enfant1)
        nouvelle_population.append(enfant2)

    population = nouvelle_population[:taille_population]
for chromosome in population:
    if fitness(chromosome) > fitness(meilleur):
        meilleur = chromosome[:]
print()
print("Meilleure cédule :")
for u in range(7):
    print("Unité", u + 1, ":", meilleur[u])

print()
print("Réserves :", calculer_reserves(meilleur))
print("Performance :", fitness(meilleur), "MW")
