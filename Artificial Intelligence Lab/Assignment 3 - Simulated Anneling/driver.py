import math
import random
import csv
from collections import deque

# File paths
engine_file = "D:/Visual Studio Code WorkShop/Python/Artificial Intelligence Lab/Assignment 3/engines.txt"     # Change path accordingly
tire_file = "D:/Visual Studio Code WorkShop/Python/Artificial Intelligence Lab/Assignment 3/tires.txt"                         # Change path accordingly
transmission_file = "D:/Visual Studio Code WorkShop/Python/Artificial Intelligence Lab/Assignment 3/transmissions.txt"         # Change path accordingly
valid_cars_file = "D:/Visual Studio Code WorkShop/Python/Artificial Intelligence Lab/Assignment 3/valid_book.csv"              # Change path accordingly

# Class representing a Car
class Car:
    def __init__(self, engine, tire, transmission, roof):
        self.engine = engine
        self.tire = tire
        self.transmission = transmission
        self.roof = roof

    def __eq__(self, other):
        return (
            self.engine == other.engine and
            self.tire == other.tire and
            self.transmission == other.transmission and
            self.roof == other.roof
        )

    def __hash__(self):
        return hash((self.engine, self.tire, self.transmission, self.roof))

    def __repr__(self):
        return f"Car(engine={self.engine}, tire={self.tire}, transmission={self.transmission}, roof={self.roof})"


# Load valid car models
valid_cars = set()
def load_cars(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if present
        for engine, tire, transmission, roof in reader:
            valid_cars.add(Car(engine, tire, transmission, roof))


# Read contents of a file into a list
def content_reader(filename):
    with open(filename) as file:
        return [line.strip() for line in file]


# Compare car with the target to calculate mismatches
def compare_with_target(car1, car2):
    mismatches = 0
    if car1.engine != car2.engine:
        mismatches += 1
    if car1.tire != car2.tire:
        mismatches += 1
    if car1.transmission != car2.transmission:
        mismatches += 1
    if car1.roof != car2.roof:
        mismatches += 1
    return mismatches


# Calculate ΔE between parent and child states
def delta_e(parent_car, child_car, target):
    return compare_with_target(parent_car, target) - compare_with_target(child_car, target)


# Calculate acceptance probability
def get_e(delta_e, t):
    return math.exp(delta_e / t)


# Load data
engines = content_reader(engine_file)
transmissions = content_reader(transmission_file)
tires = content_reader(tire_file)
roofs = ["Sunroof", "Moonroof", "Noroof"]
load_cars(valid_cars_file)

# Start and goal states
start_car = Car("EFI", "Danlop", "AT", "Noroof")
goal_car = Car("V12", "Pirelli", "CVT", "Sunroof")

# Simulated Annealing with BFS
frontier = deque([start_car])
seen = set([start_car])
level = 0
goal_reached = False

while frontier and not goal_reached:
    level += 1
    next_frontier = deque()
    while frontier:
        current_car = frontier.popleft()

        # Generate children by changing each component
        for engine in engines:
            candidate_car = Car(engine, current_car.tire, current_car.transmission, current_car.roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(f"Goal reached in {level} years.")
                    goal_reached = True
                    break
                delta = delta_e(current_car, candidate_car, goal_car)
                if delta > 0 or random.uniform(0, 1) <= get_e(delta, 1 / level):
                    next_frontier.append(candidate_car)
                    seen.add(candidate_car)

        for tire in tires:
            candidate_car = Car(current_car.engine, tire, current_car.transmission, current_car.roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(f"Goal reached in {level} years.")
                    goal_reached = True
                    break
                delta = delta_e(current_car, candidate_car, goal_car)
                if delta > 0 or random.uniform(0, 1) <= get_e(delta, 1 / level):
                    next_frontier.append(candidate_car)
                    seen.add(candidate_car)

        for transmission in transmissions:
            candidate_car = Car(current_car.engine, current_car.tire, transmission, current_car.roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(f"Goal reached in {level} years.")
                    goal_reached = True
                    break
                delta = delta_e(current_car, candidate_car, goal_car)
                if delta > 0 or random.uniform(0, 1) <= get_e(delta, 1 / level):
                    next_frontier.append(candidate_car)
                    seen.add(candidate_car)

        for roof in roofs:
            candidate_car = Car(current_car.engine, current_car.tire, current_car.transmission, roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(f"Goal reached in {level} years.")
                    goal_reached = True
                    break
                delta = delta_e(current_car, candidate_car, goal_car)
                if delta > 0 or random.uniform(0, 1) <= get_e(delta, 1 / level):
                    next_frontier.append(candidate_car)
                    seen.add(candidate_car)

        if goal_reached:
            break

    frontier = next_frontier

if not goal_reached:
    print("Goal state not reachable.")
