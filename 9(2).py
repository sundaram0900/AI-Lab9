import random

GROUP_SIZE = 100
CHARACTERS = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''
TARGET_PHRASE = "Sundar"

class Entity:
    def __init__(self, genes):
        self.genes = genes
        self.score = self.evaluate_fitness()

    @classmethod
    def random_gene(cls):
        return random.choice(CHARACTERS)

    @classmethod
    def generate_dna(cls):
        length = len(TARGET_PHRASE)
        return [cls.random_gene() for _ in range(length)]

    def breed(self, partner):
        offspring_genes = []
        for gene1, gene2 in zip(self.genes, partner.genes):
            chance = random.random()
            if chance < 0.45:
                offspring_genes.append(gene1)
            elif chance < 0.90:
                offspring_genes.append(gene2)
            else:
                offspring_genes.append(self.random_gene())
        return Entity(offspring_genes)

    def evaluate_fitness(self):
        return sum(1 for g1, g2 in zip(self.genes, TARGET_PHRASE) if g1 != g2)

def create_population():
    return [Entity(Entity.generate_dna()) for _ in range(GROUP_SIZE)]

def pick_parents(group):
    return random.sample(group, k=2)

def recombine(parent1, parent2):
    child_genes = []
    for g1, g2 in zip(parent1.genes, parent2.genes):
        chance = random.random()
        if chance < 0.45:
            child_genes.append(g1)
        elif chance < 0.90:
            child_genes.append(g2)
        else:
            child_genes.append(Entity.random_gene())
    return Entity(child_genes)

def modify_genes(genes):
    return [random.choice(CHARACTERS) if random.random() < 0.1 else gene for gene in genes]

def mutate_entity(entity):
    mutated_genes = modify_genes(entity.genes)
    return Entity(mutated_genes)

def evolve():
    generation_num = 1
    solution_found = False
    population = create_population()

    while not solution_found:
        population = sorted(population, key=lambda x: x.score)
        if population[0].score == 0:
            solution_found = True
            break

        next_gen = []
        next_gen.extend(population[:int(0.1 * GROUP_SIZE)])

        for _ in range(int(0.9 * GROUP_SIZE)):
            p1, p2 = pick_parents(population)
            offspring = recombine(p1, p2)
            next_gen.append(offspring)

        population = next_gen

        print("Generation: {}\tPhrase: {}\tScore: {}".format(
            generation_num, "".join(population[0].genes), population[0].score))

        generation_num += 1

    print("Final Generation: {}\tPhrase: {}\tScore: {}".format(
        generation_num, "".join(population[0].genes), population[0].score))

if __name__ == '__main__':
    evolve()
