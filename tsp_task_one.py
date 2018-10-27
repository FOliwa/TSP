from bs4 import BeautifulSoup
from math import inf
import timeit, time
import itertools


class BaseParser():
    def __init__(self, data_type, number_of_nodes, test):
        self.file_dict = {
            'symetric': {
                '14': 'symetric_data/burma14.xml',
                '48': 'symetric_data/gr48.xml',
            },
            'asymetric': {
                '17': 'asymetric_data/br17.xml',
                '33': 'asymetric_data/ftv33.xml',
            }
        }
        self.adjacency_matrix = []
        self.test_matrix = [[0, 3, 5, 7],
                            [3, 0, 4, 9],
                            [5, 4, 0, 1],
                            [7, 9, 1, 0]]
        if test:
            self.adjacency_matrix = self.test_matrix
            self.display_matrix()
        else:
            self.prepare_adjacency_matrix(self.file_dict[data_type][number_of_nodes])
            self.display_matrix()

    def prepare_adjacency_matrix(self, file):
        with open(file) as file_hendler:
            content = BeautifulSoup(file_hendler, "xml")
        cities = content.find_all('vertex')
        # +1 do liczby miast zeby uninac bledu OutOfRange error.
        # W plikach XML brakuje indeksu miasta w ktorym aktualnie sie znajdujemy
        number_of_cities = len(cities[0].find_all('edge'))+1
        for i in range(len(cities)):
            self.adjacency_matrix.append([0]*number_of_cities)
            roads = cities[i].find_all('edge')
            for road in roads:
                self.adjacency_matrix[i][int(road.text)] = int(float(road.get("cost")))

    def display_matrix(self):
        for row in self.adjacency_matrix:
            print(row)


class Tsp(BaseParser):
    def __init__(self, data_type='symetric', number_of_nodes = '14', test=False):
        BaseParser.__init__(self,data_type, number_of_nodes, test)
        self.time_passed = None
        self.lowest_cost = inf
        self.best_route = []
        self.run()

    def run(self):
        self.lowest_cost, self.best_route = self.calculate_symetric_cost(self.adjacency_matrix)
        self.print_results()

    def print_results(self):
        print("=================== BEST ROUTE =========================")
        print(self.best_route, ' --->', self.lowest_cost)
        print("======= OBLICZENIA ZAJELY ", self.time_passed, " ============")

    # Dla symetrycznych nie trzba przeszukiwac wszystkich
    # mozliwych permutacji: [1,2,3] = [2,3,1] = [3,1,2]
    def calculate_symetric_cost(self, data_matrix):
        import ipdb; ipdb.set_trace()
        cost = inf
        best_route = []
        routes = itertools.permutations(list(range(1, len(data_matrix[0]))))
        for route in routes:
            route = list(route)
            route.insert(0, 0)
            new_travel_cost = 0
            for i in range(len(route)-1):
                new_travel_cost += data_matrix[route[i]][route[i+1]]
            new_travel_cost += data_matrix[route[len(route)-1]][0]
            if new_travel_cost < cost:
                cost, best_route = new_travel_cost, route
        return cost, best_route

    # Dla niesymetrycznych danych przeszukujemy caly zestaw permutacji
    def calculate_asymetric_cost(self, data_matrix):
        cost = inf
        best_route = []
        routes = itertools.permutations(list(range(len(data_matrix[0]))))
        for route in routes:
            new_travel_cost = 0
            for i in range(len(route) - 1):
                new_travel_cost += data_matrix[route[i]][route[i + 1]]
            new_travel_cost += data_matrix[route[len(route) - 1]][0]
            if new_travel_cost < cost:
                cost, best_route = new_travel_cost, route
        return cost, best_route

def what_time(method):
    def timed(*args, **kwargs):
        start_time = timeit.default_timer()
        cost, best_route = method(*args, **kwargs)
        return cost, best_route, timeit.default_timer() - start_time


tsp = Tsp('symetric', '14', True)

