import random

capacity = 50
weights = [10, 20, 30, 40, 50]
values = [60, 80, 100, 120, 140]
pop_size = 50
num_generations = 100
mutation_prob = 0.1

def create_chromosome():
    return [random.choice([0, 1]) for _ in range(len(weights))]

def create_population():
    return [create_chromosome() for _ in range(pop_size)]

def evaluate(chromosome):
    total_val = sum(gene * val for gene, val in zip(chromosome, values))
    total_wt = sum(gene * wt for gene, wt in zip(chromosome, weights))
    return 0 if total_wt > capacity else total_val

def select_mates(population):
    scores = [evaluate(chromo) for chromo in population]
    total_score = sum(scores)
    selected = []
    while len(selected) < pop_size:
        idx = random.choices(range(len(population)), weights=scores)[0]
        selected.append(population[idx])
    return selected

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def mutate(chromosome):
    idx = random.randint(0, len(chromosome) - 1)
    chromosome[idx] = 1 - chromosome[idx]

def apply_mutations(population):
    for chromo in population:
        if random.random() < mutation_prob:
            mutate(chromo)

def genetic_algo():
    population = create_population()
    for _ in range(num_generations):
        parents = select_mates(population)
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = crossover(parents[i], parents[i + 1])
                offspring.extend([child1, child2])
        apply_mutations(offspring)
        population = offspring
    best = max(population, key=evaluate)
    return best, evaluate(best)

best_solution, best_value = genetic_algo()
print("Best Solution:", best_solution)
print("Best Value:", best_value)
