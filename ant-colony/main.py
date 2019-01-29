from aco import ACO, Graph
from data.sym import s_14, s_48, s_130
from data.asym import a_17, a_33, a_64, a_170

# distance_matrix = s_14.data      # 3323
# distance_matrix = s_48.data    # 5046
# distance_matrix = s_130.data   # 6110
#
distance_matrix = a_17.data    # 39
# distance_matrix = a_33.data    # 1286
# distance_matrix = a_64.data    # 1839
# distance_matrix = a_170.data


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


def main():
    cost_matrix = distance_matrix
    rank = len(distance_matrix[0])
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))


if __name__ == '__main__':
    main()