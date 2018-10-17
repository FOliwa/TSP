from bs4 import BeautifulSoup

#file = "symetric_data/burma14.xml"
file = "symetric_data/gr48.xml"


def prepare_adjacency_matrix(file):
    adjacency_matrix = []
    with open(file) as file_hendler:
        content = BeautifulSoup(file_hendler, "xml")
    towns = content.find_all('vertex')
    for town in towns:
        roads = town.find_all('edge')
        print('###################################')
        for road in roads:
            print(road.get('cost'))
    # print(towns[4].find_all('edge'))
    # for i in range(len(towns)):
    #     adjacency_matrix.append(towns[i])
    #
    # display_matrix(adjacency_matrix)


def display_matrix(matrix):
    for row in matrix:
        print(row)


prepare_adjacency_matrix(file)

