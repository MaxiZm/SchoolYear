import time
from deap import base, creator, tools
import random
import json
from multiprocessing import Pool, cpu_count
from Schedule import Schedule
from Rater import Rater
import app

# Load data from file
with open('data.json') as f:
    data = json.load(f)

print(cpu_count(), "threads detected")


rater = Rater(data)
toolbox = base.Toolbox()




class aSchedule(Schedule):
    def __init__(self):
        super().__init__(data)
        self.randomly_generate()
        self.fitness = creator.FitnessMax()



# Define evaluation function
def evaluate(individual):

    return rater.rate_schedule(individual),  # Note the comma, it's important for DEAP

# Mutation function (might need adjustments based on actual schedule representation)
def mutate(individual, indpb):
    # Your existing mutate function seems to expect a schedule's format,
    # Ensure individual is in correct format to apply mutations
    for key, class_schedule in individual.schedule.items():
        for day in range(len(class_schedule)):
            if random.random() < indpb:
                data_class = list(filter(lambda x: x["name"] == key, data["classes"]))[0]

                action = random.choice(("append", "remove", "replace"))

                if action == "append":
                    individual.schedule[key][day] += [random.choice(data_class["curriculum"])]

                elif action == "remove":
                    individual.schedule[key][day].pop(random.randint(0, len(individual.schedule[key][day]) - 1))

                elif action == "replace":
                    individual.schedule[key][day][random.randint(0, len(individual.schedule[key][day]) - 1)] = random.choice(data_class["curriculum"])

                # Assuming you have a method to choose a valid lesson for mutation

    return individual,

# Crossover function (might need adjustments based on actual schedule representation)
def crossover(ind1, ind2):
    if random.random() < 0.5:
        crossover_point = random.randint(1, len(ind1.schedule) - 1)
        for i, key in enumerate(ind1.schedule.keys()):
            if i >= crossover_point:
                ind1.schedule[key], ind2.schedule[key] = ind2.schedule[key], ind1.schedule[key]

    else:
        class_ = random.choice(list(ind1.schedule.keys()))
        crossover_point = random.randint(1, len(ind1.schedule[class_]) - 1)
        for i in range(crossover_point, len(ind1.schedule[class_])):
            ind1.schedule[class_][i], ind2.schedule[class_][i] = ind2.schedule[class_][i], ind1.schedule[class_][i]

    return ind1, ind2



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
toolbox.register("population", tools.initRepeat, list, aSchedule)
toolbox.register("mate", crossover)
toolbox.register("mutate", mutate, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)




def population_mutate(mutant):
    if random.random() < 0.2:
        toolbox.mutate(mutant)
        del mutant.fitness.values
    return mutant


def population_crossover(child1child2):
    child1, child2 = child1child2

    if random.random() < 0.5:
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values

    return child1, child2

def main():
    # toolbox = base.Toolbox()
    pool = Pool(processes=cpu_count())
    toolbox.register("map", pool.map)

    # Individual initialization (needs to be adapted to create a valid schedule)


    pop = toolbox.population(n=200)

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit


    initial_time = time.time()

    fitnesses_history = [  ]


    # Define the evolution loop
    generations = 200
    for gen in range(generations):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))

        offspring2 = toolbox.map(population_crossover, zip(offspring[::2], offspring[1::2]))
        offspring = []

        for i in offspring2:
            for j in i:
                offspring.append(j)

        offspring = toolbox.map(population_mutate, offspring)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        if gen % 10 == 9:
            print(gen + 1, generations, sep=" / ")

        fitnesses_history.append(max(fitnesses))

    best_schedule = tools.selBest(pop, 1)[0]
    print("Best Schedule:", best_schedule.schedule)
    print("Fitness:", best_schedule.fitness.values[0])
    print("Generations/second:", generations/(time.time()-initial_time))

    pool.close()

    with open("best_solution.json", "w") as f:
        json.dump(best_schedule.schedule, f, ensure_ascii=False, indent=4)

    app.main(best_schedule.schedule, range(generations), fitnesses_history)


if __name__ == "__main__":
    main()
