from bs4 import BeautifulSoup
from math import inf
import itertools

file_dict = {
    'symetric': {
        '14': 'symetric_data/burma14.xml',
        '48': 'symetric_data/gr48.xml',
    },
    'asymetric': {
        '17': 'asymetric_data/br17.xml',
        '33': 'asymetric_data/ftv33.xml',
    }
}


class Tsp:

    def __init__(self, file):
        self.file = file
        self.lowest_route = inf
        self.lowest_cost = []
        self.number_of_cities = 0
        self.adjacency_matrix = []

    def prepare_adjacency_matrix(self):
        with open(self.file) as file_hendler:
            content = BeautifulSoup(file_hendler, "xml")
        cities = content.find_all('vertex')
        self.number_of_cities = len(cities[0].find_all('edge'))+1     # +1 to avoid OutOfRange error
        print(self.number_of_cities)
        for i in range(len(cities)):
            self.adjacency_matrix.append([0]*self.number_of_cities)
            roads = cities[i].find_all('edge')
            for road in roads:
                self.adjacency_matrix[i][int(road.text)] = int(float(road.get("cost")))

    def display_matrix(self):
        for row in self.adjacency_matrix:
            print(row)

    def prepare_dict_of_nodes(self, file):
        pass


    def calculate_cost(self, symetric=True):
        # import ipdb; ipdb.set_trace()
        if symetric:
            all_travels_costs = []
            routes = itertools.permutations(list(range(self.number_of_cities)))
            for route in routes:
                travel_cost = 0
                for i in range(0, len(route)-2):
                    travel_cost += self.adjacency_matrix[route[i]][route[i+1]]
                travel_cost += self.adjacency_matrix[route[len(route)-1]][0]

                if travel_cost < self.lowest_cost:
                    self.lowest_cost = travel_cost
                    self.lowest_route = route
                    print(route, ' --->',travel_cost)
        else:
            pass
        print("===============BEST ROUTE=====================")
        print(self.lowest_route, ' --->', self.lowest_cost)
        return 1


tsp = Tsp(file_dict['symetric']['14'])
tsp.prepare_adjacency_matrix()
tsp.display_matrix()
tsp.calculate_cost()
