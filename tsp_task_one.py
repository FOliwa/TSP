from bs4 import BeautifulSoup
from math import inf
import timeit
import datetime
import itertools
from decorators import what_time, profile


file_dict = {
    'symetric': {
        '5': 'symetric_data/test5.xml',
        '7': 'symetric_data/test7.xml',
        '10': 'symetric_data/test10.xml',
        '11': 'symetric_data/test11.xml',
        '13': 'symetric_data/test13.xml',
        '14': 'symetric_data/burma14.xml',  # 3323
        '48': 'symetric_data/gr48.xml',
    },
    'asymetric': {
        '17': 'asymetric_data/br17.xml',
        '33': 'asymetric_data/ftv33.xml',
    }
}

test_matrix = [[0, 20, 42, 25],
               [20, 0, 30, 34],
               [42, 30, 0, 10],
               [25, 34, 10, 0]]     #Min cost = 85

class BaseParser():
    def __init__(self, data_type, number_of_nodes, test):
        self.adjacency_matrix = []
        self.best_route = []
        self.data_type = data_type
        self.test = test
        self.time_passed = None
        self.name = data_type + '_' + number_of_nodes
        self.lowest_cost = inf
        if test:
            self.adjacency_matrix = test_matrix
            self.display_matrix()
        else:
            self.prepare_adjacency_matrix(file_dict[data_type][number_of_nodes])
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

    def save_results(self, results):
        with open('.\\results\\' + self.name + '.txt', 'a') as file:
            file.write(str(results) + '\n')

    def print_results(self, results):
        print("=================== BEST ROUTE =========================")
        print("-----> KOSZT: ", results[0])
        print("-----> TRASA: ", results[1])
        print("========================================================")


class TspBrutForce(BaseParser):
    def __init__(self, data_type='symetric', number_of_nodes = '14', test=False):
        BaseParser.__init__(self,data_type, number_of_nodes, test)
        self.run()

    def run(self):
        print("============ OBLICZANIE TSP METODA BF ==================")
        if self.data_type == 'symetric':
            results = self.brut_force_calculation_for_symetric(
                self.adjacency_matrix)
        elif self.data_type == 'asymetric':
            results = self.brut_force_calculation_for_asymetric(
                self.adjacency_matrix)
        else:
            return "BLAD NAZWY PLIKU"
        print("================= KONIEC OBLICZEN ======================")
        self.print_results(results)
        if not self.test:
            self.save_results(results)

    # Dla symetrycznych nie trzba przeszukiwac wszystkich
    # mozliwych permutacji: [1,2,3] = [2,3,1] = [3,1,2]
    @profile
    @what_time
    def brut_force_calculation_for_symetric(self, data_matrix):
        cost = inf
        best_route = []
        lenght = len(data_matrix[0])
        routes = itertools.permutations(range(1, lenght))
        for route in routes:
            new_travel_cost = data_matrix[0][route[0]]
            for i in range(lenght-2):
                new_travel_cost += data_matrix[route[i]][route[i+1]]
            new_travel_cost += data_matrix[route[lenght-2]][0]
            if new_travel_cost < cost:
                cost, best_route = new_travel_cost, route
        return cost, best_route

    # Dla niesymetrycznych danych przeszukujemy caly zestaw permutacji
    def brut_force_calculation_for_asymetric(self, data_matrix):
        cost = inf
        best_route = []
        lenght = len(data_matrix[0])
        routes = itertools.permutations(range(lenght))
        for route in routes:
            new_travel_cost = 0
            for i in range(lenght - 1):
                new_travel_cost += data_matrix[route[i]][route[i + 1]]
            new_travel_cost += data_matrix[route[lenght - 1]][route[0]]
            if new_travel_cost < cost:
                cost, best_route = new_travel_cost, route
        return cost, best_route


class TspDynamicProgramming(BaseParser):
    def __init__(self, data_type='symetric', number_of_nodes='14', test=False):
        BaseParser.__init__(self, data_type, number_of_nodes, test)
        self.number_of_cities = len(self.adjacency_matrix[0])
        # Maska bitowa wypelniona jedynkami oznacza ze wszystkie miasta zostaly odwiedzone
        # Dla 4 miast maska ma postac 1111 
        self.VISITED_ALL = (1 << self.number_of_cities) - 1   
        # Tablica zawierajaca rezultaty dla konkrtenych par maska-pozycja - pomocne do optymalizacji kodu
        # Wratosci poczatkowe ustawione na -1.
        self.dp_matrix = [[-1 for x in range(self.number_of_cities)] for y in range(2**self.number_of_cities)]
        self.run()

    def run(self):
        print("============ OBLICZANIE TSP METODA DP ==================")
        results = self.dynamic_programming_calculations(1, 0)
        print("Koszt minimalny to : ", results)
        print("================= KONIEC OBLICZEN ======================")
        # self.save_results(results)

    def dynamic_programming_calculations(self, mask, possition):    # maska to 2^N, pozycji mamy N - zlozonosc [2^N]*N
        # import ipdb; ipdb.set_trace()
        if mask == self.VISITED_ALL:
            return self.adjacency_matrix[possition][0]

        # Sprawdzenie czy nie obliczm jakiejs sciezki kolejny raz
        # Jesli wartosc w tablicy dp jest rozna -1 to oznacza ze dla tej maski i pozycji mam juz wyliczona wartosc
        if self.dp_matrix[mask][possition] != -1:
            return self.dp_matrix[mask][possition]
        
        cost = inf
        # Proba odwiedzenia miasta w ktorym podroznik jeszcze nie byl
        for city in range(self.number_of_cities):
            if (mask&(1<<city)) == 0:
                newCost = self.adjacency_matrix[possition][city] + self.dynamic_programming_calculations(mask | (1<<city), city)
                cost = min(cost, newCost)
        self.dp_matrix[mask][possition] = cost
        return cost


# X = TspBrutForce(test=True)
Y = TspDynamicProgramming('symetric', '5', False)
