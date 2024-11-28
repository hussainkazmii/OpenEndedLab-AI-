import random

# Meal data: each meal has a name and a calorie count
MEALS = [
    {"name": "Oatmeal", "calories": 150},
    {"name": "Salad", "calories": 200},
    {"name": "Grilled Chicken", "calories": 350},
    {"name": "Rice", "calories": 300},
    {"name": "Fruits", "calories": 100},
    {"name": "Pasta", "calories": 400},
    {"name": "Smoothie", "calories": 250},
]

TARGET_CALORIES = 1500  # Daily calorie goal
POPULATION_SIZE = 10  # Number of meal plans
GENERATIONS = 50  # Number of generations
MUTATION_RATE = 0.1  # Probability of mutation

# Generate a random meal plan (chromosome)
def generate_chromosome():
    return [random.randint(0, 1) for _ in range(len(MEALS))]

# Fitness function: minimize the absolute difference from the target calories
def fitness_function(chromosome):
    total_calories = sum(meal["calories"] * gene for meal, gene in zip(MEALS, chromosome))
    return -abs(TARGET_CALORIES - total_calories)  # Negative for maximization

# Selection: Choose parents using tournament selection
def select_parents(population, fitness_scores):
    selected = random.sample(list(zip(population, fitness_scores)), 3)
    return max(selected, key=lambda x: x[1])[0]

# Crossover: Single-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

# Mutation: Flip a gene (include or exclude a meal)
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]  # Flip 0 to 1 or 1 to 0
    return chromosome

# Genetic Algorithm
def genetic_algorithm():
    # Initialize population
    population = [generate_chromosome() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        # Evaluate fitness of the population
        fitness_scores = [fitness_function(chrom) for chrom in population]
        
        # Print the best fitness in the current generation
        best_fitness = max(fitness_scores)
        best_individual = population[fitness_scores.index(best_fitness)]
        print(f"Generation {generation + 1}: Best Fitness = {-best_fitness}")

        # Selection, Crossover, and Mutation
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parents(population, fitness_scores)
            parent2 = select_parents(population, fitness_scores)
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring)
            new_population.append(offspring)

        # Replace the old population with the new one
        population = new_population

    # Return the best solution
    best_solution = best_individual
    total_calories = sum(meal["calories"] * gene for meal, gene in zip(MEALS, best_solution))
    return best_solution, total_calories

if __name__ == "__main__":
    print(f"Target Calories: {TARGET_CALORIES}")
    solution, total_calories = genetic_algorithm()
    print("\nOptimal Meal Plan:")
    for meal, gene in zip(MEALS, solution):
        if gene == 1:
            print(f"- {meal['name']} ({meal['calories']} calories)")
    print(f"\nTotal Calories: {total_calories}")
    print(f"Deviation from Target: {abs(TARGET_CALORIES - total_calories)} calories")
