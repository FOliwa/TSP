from bs4 import BeautifulSoup
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
        self.adjacency_matrix = []

    def prepare_adjacency_matrix(self):
        with open(self.file) as file_hendler:
            content = BeautifulSoup(file_hendler, "xml")
        towns = content.find_all('vertex')
        size = len(towns[0].find_all('edge'))+1     # +1 to avoid OutOfRange error
        for i in range(len(towns)):
            self.adjacency_matrix.append([0]*size)
            roads = towns[i].find_all('edge')
            for road in roads:
                self.adjacency_matrix[i][int(road.text)] = int(float(road.get("cost")))

    def display_matrix(self):
        for row in self.adjacency_matrix:
            print(row)

    def prepare_dict_of_nodes(self, file):
        pass

    def generate_symetric_routes(self):
        cities_indexes = [index for index in range(2, len(self.adjacency_matrix[0])+1)]
        # tutaj jest problem - uzywa za duzo pamieci
        # Moze generator??
        routes = list(map(list, itertools.permutations(cities_indexes)))
        for x in routes:
            x.insert(0, 1)
        return routes

    def calculate_cost(self):
        # import ipdb; ipdb.set_trace()
        routes = self.generate_symetric_routes()
        all_travels_costs = []
        for route in routes:
            travel_cost = 0
            for i in range(1, len(route)-1):
                travel_cost += self.adjacency_matrix[route[i]][route[i+1]]
            travel_cost += self.adjacency_matrix[route[len(route)]][0]


tsp = Tsp(file_dict['symetric']['14'])
tsp.prepare_adjacency_matrix()
tsp.calculate_cost()
