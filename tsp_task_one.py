from bs4 import BeautifulSoup
from math import inf
import timeit, time
import itertools
from decorators import what_time, profile


class BaseParser():
    def __init__(self, data_type, number_of_nodes, test):
        self.file_dict = {
            'symetric': {
                '5': 'symetric_data/test5.xml',
                '7': 'symetric_data/test7.xml',
                '10': 'symetric_data/test10.xml',
                '11': 'symetric_data/test11.xml',
                '13': 'symetric_data/test13.xml',
                '14': 'symetric_data/burma14.xml',  #3323
                '48': 'symetric_data/gr48.xml',
            },
            'asymetric': {
                '17': 'asymetric_data/br17.xml',
                '33': 'asymetric_data/ftv33.xml',
            }
        }
        self.adjacency_matrix = []
        self.test_matrix = [[0, 30, 5, 1],
                            [30, 0, 1, 9],
                            [5, 1, 0, 9],
                            [1, 9, 9, 0]]
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
        self.name = data_type + '_' + number_of_nodes
        self.time_passed = None
        self.lowest_cost = inf
        self.best_route = []
        self.run()

    def run(self):
        print("============ OBLICZANIE TSP METODA BF ==================")
        results = self.calculate_symetric_cost(self.adjacency_matrix)
        print("================= KONIEC OBLICZEN ======================")
        self.print_results(results)
        self.save_results(results)

    def save_results(self, results):
        with open('.\\results\\' + self.name + '.txt', 'a') as file:
            file.write(str(results) + '\n')

    def print_results(self, results):
        print("=================== BEST ROUTE =========================")
        print("KOSZT: ", results[0], " --- TRASA: ", results[1])
        print("======= OBLICZENIA ZAJELY ", results[2], " ============")

    # Dla symetrycznych nie trzba przeszukiwac wszystkich
    # mozliwych permutacji: [1,2,3] = [2,3,1] = [3,1,2]
    @profile
    @what_time
    def calculate_symetric_cost(self, data_matrix):
        # import ipdb; ipdb.set_trace()
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
            lenght = len(route)
            new_travel_cost = 0
            for i in range(lenght - 1):
                new_travel_cost += data_matrix[route[i]][route[i + 1]]
            new_travel_cost += data_matrix[route[lenght - 1]][0]
            if new_travel_cost < cost:
                cost, best_route = new_travel_cost, route
        return cost, best_route


X = Tsp('symetric', '14', False)