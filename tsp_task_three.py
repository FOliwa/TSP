import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
from data.sym import s_14, s_48, s_130
from data.asym import a_17, a_33, a_64, a_170
from decorators import profile

class City:
    """
    Reprezenation of each node/city in the graph
    """
    def __init__(self, index):
        self.city_index = index

    def distance(self, city):
        return distance_matrix[self.city_index][city.city_index]

    def __repr__(self):
        return "(" + str(self.city_index) + ")"


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def route_distance(self):
        if self.distance == 0:
            path_distance = 0
            for i in range(0, len(self.route)):
                from_city = self.route[i]
                to_city = None
                if i + 1 < len(self.route):
                    to_city = self.route[i + 1]
                else:
                    to_city = self.route[0]
                path_distance += from_city.distance(to_city)
            self.distance = path_distance
        return self.distance

    def route_fitness(self):
        """
        larger fitness score is better
        """
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness


def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route


def initial_population(pop_size, city_list):
    population = []
    for i in range(0, pop_size):
        population.append(create_route(city_list))
    return population


def rank_routes(population):
    fitness_results = {}
    for i in range(0, len(population)):
        fitness_results[i] = Fitness(population[i]).route_fitness()
    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)    # sortowanie od najwiekszego do najmniejszego po fitnesie


def selection(population_rank, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(population_rank), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()     # kumulatywnie sumuje wszystko z kolumny "Fitness" - tworze przedzialy
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()    # df.Fitness.sum = suma wsystkich elementow z tej kolumny

    for i in range(0, elite_size):
        selection_results.append(population_rank[i][0])      # Doodaje do wyniku najlepsze chromosomy z obcenej populacji
    for i in range(0, len(population_rank)-elite_size):      # Selekcja do krzyzowania  - losuje przedzialami w oparciu o fitness
        pick = 100*random.random()      # Losuje randomowa wartosc od 0-100
        for i in range(0, len(population_rank)):
            if pick <= df.iat[i,3]:     # Z biblioteki pandas - wybieram konkretna komorke z macierzy o indeksie [i , 3]
                selection_results.append(population_rank[i][0])
                break
    return selection_results     # Zwracam indeksy wybranych chromosomow


def mating_pool(population, selection_results):
    mp = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mp.append(population[index])
    return mp


def breed(parent1, parent2):
    child = []
    child_p1 = []
    child_p2 = []

    gene_a = int(random.random() * len(parent1))
    gene_b = int(random.random() * len(parent1))

    start_gene = min(gene_a, gene_b)      # Kolejnosc jest istotna- tutaj zawsze musze isc od najmniejszego do najwiekszego
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child_p1.append(parent1[i])      # Kopiuje kolejne miasta z chromosomu nr 1

    child_p2 = [item for item in parent2 if item not in child_p1]     # Sprawdzam po kolei geny w chromosomie 2 i jak nie ma ich w dziecku to kopiuje
    child = child_p1 + child_p2
    return child


def breed_population(matingpool, elite_size):
    children = []
    length = len(matingpool) - elite_size
    pool = random.sample(matingpool, len(matingpool))   # Przemieszam elementy na liscie zeby nie wystepowaly w kolejnosci
    for i in range(0, elite_size):
        children.append(matingpool[i])      # Tutaj przenosze najlepsze jednostki z poprzedniej populacji. One nadal ida do krzyzowania

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])   # biore dwa kolejne elemety i przekazuje do krzyzowania
        children.append(child)
    return children


def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if (random.random() < mutation_rate):
            swap_with = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swap_with]

            individual[swapped] = city2
            individual[swap_with] = city1
    return individual


def mutate_population(population, mutation_rate):
    mutated_population = []

    for index in range(0, len(population)):
        mutated_index = mutate(population[index], mutation_rate)
        mutated_population.append(mutated_index)
    return mutated_population


def get_next_generation(current_generation, elite_size, mutation_rate):
    population_rank = rank_routes(current_generation)
    selection_results = selection(population_rank, elite_size)
    matingpool = mating_pool(current_generation, selection_results)
    children = breed_population(matingpool, elite_size)
    get_next_generation = mutate_population(children, mutation_rate)
    return get_next_generation


def genetic_algorithm(population, pop_size, elite_size, mutation_rate, numbers_of_generations):
    pop = initial_population(pop_size, population)
    print("Initial distance: " + str(round(1 / rank_routes(pop)[0][1])))

    for i in range(0, numbers_of_generations):
        pop = get_next_generation(pop, elite_size, mutation_rate)

    print("Final distance: " + str(round(1 / rank_routes(pop)[0][1])))
    best_route_index = rank_routes(pop)[0][0]
    best_route = pop[best_route_index]
    print("ROUTE: ", best_route)


def genetic_algorithm_plot(city_list, pop_size, elite_size, mutation_rate, numbers_of_generations):
    pop = initial_population(pop_size, city_list)
    progress = []
    progress.append(1 / rank_routes(pop)[0][1])

    for i in range(0, numbers_of_generations):
        pop = get_next_generation(pop, elite_size, mutation_rate)
        progress.append(1 / rank_routes(pop)[0][1])

    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
    print("BEST DISTANCE: ", round(min(progress)))


test_matrix = [[0, 1, 3, 4, 5],
             [1, 0, 1, 4, 8],
             [3, 1, 0, 5, 1],
             [4, 4, 5, 0, 2],
             [5, 8, 1, 2, 0]]

# distance_matrix = s_14.data      # 3323
distance_matrix = a_170.data    # 5046
# distance_matrix = s_130.data   # 6110

# distance_matrix = a_17.data    # 39
# distance_matrix = a_33.data    # 1286
# distance_matrix = a_64.data    # 1839

cities = [City(i) for i in range(0, len(distance_matrix[0]))]
genetic_algorithm(cities, 150, 10, 0.01, 300)
# genetic_algorithm(cities, 200, 50, 0.05, 300)


# dorigo -> alg. mrowkowy