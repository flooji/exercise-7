import math
import tsplib95
import networkx as nx

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""


class Environment:
    def __init__(self, rho):

        self.rho = rho

        # Initialize the environment topology
        self.topology = tsplib95.load('att48-specs/att48.tsp')
        self.dimension = self.topology.dimension

        # Initialize the pheromone map in the environment
        self.pheromone_map = []

    # Initialize the pheromone trails in the environment
    def initialize_pheromone_map(self, no_ants):
        # Pheromone trails are initialized to a value slightly higher
        # than the expected amount of pheromone deposited by the ants in one iteration

        initial_value = 1  # this initial value is taken from the book Ant Colony Optimization, p. 13
        for i in range(self.dimension):
            row = [initial_value] * self.dimension
            self.pheromone_map.append(row)
        # print("Initialized pheromone map: ", self.pheromone_map)

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants):
        # Step 1: Pheromone is first removed from all arcs (pheromone evaporation)
        for i, row in enumerate(self.pheromone_map):
            for j, arc in enumerate(row):
                # Simulates evaporation of pheromones
                self.pheromone_map[i][j] *= (1 - self.rho)

        # Step 2: Pheromone is then added on the arcs the ants have crossed in their tours
        for ant in ants:
            for i, location in enumerate(ant.visited_locations):
                deposited_pheromone = 1 / ant.travelled_distance
                x = ant.visited_locations[i - 1] - 1
                y = ant.visited_locations[i] - 1
                self.pheromone_map[x][y] += deposited_pheromone
                self.pheromone_map[y][x] += deposited_pheromone

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.pheromone_map

    # Get the environment topology
    def get_possible_locations(self):
        return list(self.topology.get_nodes())
