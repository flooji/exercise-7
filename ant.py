# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
import random
from math import sqrt

from tsplib95.utils import nint


class Ant:
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.travelled_distance = 0
        self.visited_locations = []

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        available_locations = self.environment.get_possible_locations()
        initial_location = self.current_location
        available_locations.remove(initial_location)
        self.visited_locations.append(initial_location)

        # Travel until all locations have been visited
        while len(available_locations) > 0:
            # Choose next location
            next_location = self.select_path(available_locations)

            # Update travelled distance
            self.travelled_distance += self.get_distance(self.current_location, next_location)

            # Move there
            self.current_location = next_location

            # Update visited and available locations
            self.visited_locations.append(next_location)
            available_locations.remove(next_location)

        # Finally the ant travels back home
        self.travelled_distance += self.get_distance(self.current_location, initial_location)

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self, available_locations):
        path_likelihoods = []

        # Calculate the likelihood for each path
        for location in available_locations:
            path_pheromone = self.environment.pheromone_map[self.current_location - 1][location - 1]
            path_distance = self.get_distance(self.current_location, location)
            path_likelihoods.append(path_pheromone ** self.alpha * (1 / path_distance) ** self.beta)

        # Calculate the sum of the likelihood scores
        total_likelihood = sum(path_likelihoods)

        # Calculate the probability of each path
        path_probabilities = [likelihood / total_likelihood for likelihood in path_likelihoods]

        # Choose a path based on its probability
        return random.choices(available_locations, path_probabilities)[0]

    # Computes the distance of a path between location i and j (based on the pseudo-euclidean distance algorithm)
    def get_distance(self, i, j):
        i_xy = self.environment.topology.node_coords[i]
        j_xy = self.environment.topology.node_coords[j]
        xd = i_xy[0] - j_xy[0]
        yd = i_xy[1] - j_xy[1]
        rij = sqrt((xd * xd + yd * yd) / 10.0)
        tij = nint(rij)
        if tij < rij:
            dij = tij + 1
        else:
            dij = tij
        return dij

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    # Resets the ant's attributes
    def reset(self):
        self.travelled_distance = 0
        self.visited_locations = []
        self.current_location = random.choice(self.environment.get_possible_locations())
