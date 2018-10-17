from itertools import permutations

def main(nodes=None, instance_size=5):
    routes = generate_routes(instance_size)
    shortestRout = calculate_cost(routes, nodes)


def generate_routes(route_lenght):
    list_of_nodes = [x for x in range(1, route_lenght+1)]
    all_possible_routes = list(map(list, permutations(list_of_nodes)))
    return all_possible_routes


def calculate_cost(routes, nodes):

    travel_costs = []

    for route in routes:
        travel_cost = 0
        for i in range(0, len(route)):
            pass
    return "DUPA"

def get_data():
    return "NOPE"