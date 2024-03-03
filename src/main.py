import pygad

from time_table import TimeTable
from fit_functions import create_fitness_func, calculate_f, calculate_g

time_table = TimeTable("dostepnosc.txt")

best_solutions = [None] * len(time_table.get_days())

for idx, day in enumerate(time_table.get_days()):
    availability_arrays = time_table.get_availability_arrays(day)
    time_blocks = time_table.get_time_blocks(day)
    unique_people = time_table.get_unique_people(day)

    # Skipping empty day
    if len(time_blocks) == 0:
        continue

    def on_generation(ga):
        print(f'Day: {day}, Generation: {ga.generations_completed}, Best solution: {ga.best_solution()[1]}')

    pop_size = 200
    chromosome_len = 144
    num_generations = 250 + 25 * len(unique_people)
    gene_space = list(unique_people.values())
    gene_space.append(0)
    
    fitness_func = create_fitness_func(availability_arrays)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=pop_size//10,
        fitness_func=fitness_func,
        sol_per_pop=pop_size,
        num_genes=chromosome_len,
        mutation_num_genes=(7, 1),
        mutation_type='adaptive',
        parent_selection_type='sss',
        gene_type = int,
        gene_space= gene_space,
        on_generation=on_generation,
    )

    ga_instance.run()
    #ga_instance.plot_fitness()

    best_solution, best_solution_fitness, _ = ga_instance.best_solution()
    print(f'Best solution: {best_solution}, Best fitness {best_solution_fitness}')
    best_solutions[idx] = (best_solution, best_solution_fitness)

final_fitness_f = 0
final_fitness_g = 0
print('====================Results====================')
for id, best_solution in enumerate(best_solutions):
    if best_solution is None:
        continue

    day = time_table.get_days()[id]
    availability_arrays = time_table.get_availability_arrays(day)
    solution, fitness = best_solution

    fitness_f = calculate_f(availability_arrays, solution)
    final_fitness_f += fitness_f

    fitness_g = calculate_g(solution)
    final_fitness_g += fitness_g

    print(f'Day: {day}, fitness "F": {fitness_f}, fitness "G": {fitness_g}')

print(f'Final fitness - F: {final_fitness_f}, G: {final_fitness_g}')

print('Saving results to the file...')
time_table.save_to_file(best_solutions, 'output.txt')
print('Results have been saved.')