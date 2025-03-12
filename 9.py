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
    return total_val if total_wt <= capacity else total_val * (capacity / total_wt)

def repair_chromosome(chromosome):
    while sum(gene * wt for gene, wt in zip(chromosome, weights)) > capacity:
        ones_indices = [i for i, gene in enumerate(chromosome) if gene == 1]
        if not ones_indices:
            break
        worst_idx = min(ones_indices, key=lambda i: values[i] / weights[i])
        chromosome[worst_idx] = 0
    return chromosome

def tournament_selection(population, k=3):
    selected = []
    while len(selected) < pop_size:
        tournament = random.sample(population, k)
        winner = max(tournament, key=evaluate)
        selected.append(winner)
    return selected

def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return repair_chromosome(child1), repair_chromosome(child2)

def swap_mutation(chromosome):
    idx1, idx2 = random.sample(range(len(chromosome)), 2)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

def apply_mutations(population):
    for chromo in population:
        if random.random() < mutation_prob:
            swap_mutation(chromo)

def genetic_algo():
    population = create_population()
    for _ in range(num_generations):
        parents = tournament_selection(population)
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = two_point_crossover(parents[i], parents[i + 1])
                offspring.extend([child1, child2])
        apply_mutations(offspring)
        population = offspring
    best = max(population, key=evaluate)
    return best, evaluate(best)

best_solution, best_value = genetic_algo()
print("Best Solution:", best_solution)
print("Best Value:", best_value)
