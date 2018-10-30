import timeit
from math import inf

def bf_setup():
    routes = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13],]
    matrix_14x14= [ [0, 153, 510, 706, 966, 581, 455, 70, 160, 372, 157, 567, 342, 398],
            [153, 0, 422, 664, 997, 598, 507, 197, 311, 479, 310, 581, 417, 376],
            [510, 422, 0, 289, 744, 390, 437, 491, 645, 880, 618, 374, 455, 211],
            [706, 664, 289, 0, 491, 265, 410, 664, 804, 1070, 768, 259, 499, 310],
            [966, 997, 744, 491, 0, 400, 514, 902, 990, 1261, 947, 418, 635, 636],
            [581, 598, 390, 265, 400, 0, 168, 522, 634, 910, 593, 19, 284, 239],
            [455, 507, 437, 410, 514, 168, 0, 389, 482, 757, 439, 163, 124, 232],
            [70, 197, 491, 664, 902, 522, 389, 0, 154, 406, 133, 508, 273, 355],
            [160, 311, 645, 804, 990, 634, 482, 154, 0, 276, 43, 623, 358, 498],
            [372, 479, 880, 1070, 1261, 910, 757, 406, 276, 0, 318, 898, 633, 761],
            [157, 310, 618, 768, 947, 593, 439, 133, 43, 318, 0, 582, 315, 464],
            [567, 581, 374, 259, 418, 19, 163, 508, 623, 898, 582, 0, 275, 221],
            [342, 417, 455, 499, 635, 284, 124, 273, 358, 633, 315, 275, 0, 247],
            [398, 376, 211, 310, 636, 239, 232, 355, 498, 761, 464, 221, 247, 0]]
    return routes, matrix_14x14

def bf_main_loop(routes, data_matrix, cost=inf, best_route=None):
    for route in routes:
        new_travel_cost = 0
        for i in range(len(route) - 1):
            new_travel_cost += data_matrix[route[i]][route[i + 1]]
        new_travel_cost += data_matrix[route[len(route) - 1]][0]
        if new_travel_cost < cost:                          # Pozbycie sie sprawdzenia tego warunku zaoszczedza 0.1 s. Znikoma kozysc...
            cost, best_route = new_travel_cost, route
    return cost, best_route

how_it_takes = timeit.timeit('bf_main_loop(*bf_setup())', setup="from __main__ import bf_setup, bf_main_loop", number=1000000000)
""" Z testu wynika ze sprawdzenie wyniku dla 1 mln sciezki wynosi okolo 5s.
    Do sprawdzenia w przypadku symetrycznych danych mamy 6 227 020 800 roznych tras [dla 14 miast mam [14 - 1]!]
    Sprawdzenie wszystkich tras [Ilosc tras * 5s]/1mln zajmie okolo 2h godziny"""
print(how_it_takes)

