def calculate_f(availability_arrays, solution):
    f = 0
    for i in range(len(solution)):
        if solution[i] == 0:
            continue

        person_id = solution[i]
        availability_array = availability_arrays[person_id]
        
        if availability_array[i] != 0:
            f += availability_array[i]
        else:
            f -= 1

    return f

def calculate_g(solution):
    g = 0
    for i in range(1, len(solution)):
        if solution[i] != solution[i-1]:
            g += 1

    return g

def create_fitness_func(availability_arrays):
    def fitness_func(ga_instance, solution, solution_idx):
        f = calculate_f(availability_arrays, solution)
        g = calculate_g(solution)

        return f - g
    return fitness_func