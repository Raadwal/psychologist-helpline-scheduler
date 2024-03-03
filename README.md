### Problem description
We are responsible for organizing the work of a helpline where psychologists are on duty. The phone operates 24 hours a day, 7 days a week, and our task is to prepare a weekly duty schedule so that, if possible, there is always one psychologist monitoring the phone. Psychologists are very busy people, so they provide us with their availability times, based on which we create the schedule. The entire schedule, as well as the availability hours of psychologists, is divided into 10-minute blocks, starting from 00:00-00:10 on Monday to the block 23:50-00:00 on Sunday. In each block, a psychologist may be unavailable, fully available (‘Yes’), or available only if necessary (‘EVENT’).

Frequent changes in phone duty are unfavorable because they create chaos in the organization. Therefore, solutions with the fewest duty changes are rewarded. It may happen that a certain block remains unstaffed; we allow this because there is a risk that we won’t have anyone available for certain time slots (no psychologist will be accessible during that time).

### Program description
The program was written using the Python programming language and the PyGAD library. PyGAD is an open-source library for building genetic algorithms and optimizing machine learning algorithms. It also works with libraries such as Keras and PyTorch. PyGAD supports various methods of crossover, mutation, and selection. Additionally, it allows optimization of different types of problems by enabling the design of custom fitness functions. It operates for both single-objective and multi-objective optimization. The use of the PyGAD library facilitated solving the problem described above.

### How the program works
The program starts by reading data from the file “dostepnosc.txt.” The TimeTable class is responsible for reading and preprocessing the data from the file. The loaded records are assigned to the appropriate day of the week and divided into 10-minute blocks. For example, a record like “Jan pn 08:00-09:00 TAK” will be split into six blocks. This class also keeps track of how many unique psychologists are available on each day of the week and assigns a unique identifier to each of them. Detailed information about specific blocks is stored in the TimeBlock class.

Our goal is to find the best schedule for the entire week. However, the assumption regarding the number of phone duty changes (start of work at 00:00 or end of work at 24:00 does not affect the fitness function) allows us to break down the problem into individual days of the week and find optimal solutions for each day. The optimal solutions for the entire week are composed of the optimal solutions for each individual day.

After loading the data, the program proceeds to search for the optimal solution for each day of the week. The algorithm’s stages include:

1. Availability arrays are created for each psychologist. The size of each array is 144, corresponding to the number of blocks that can divide a given day. If a psychologist has the following status in the i-th block:
- “YES” (TAK), the value at the i-th position in the array is 1.
- “EVENT” (EWENT), the value at the i-th position is 0.5.
- Otherwise, the value at the i-th position is -1.
2. Creation of methods used in the fitness function. These methods calculate the fitness value and require availability arrays, which are created for each day. Therefore, these methods need to be updated as the algorithm progresses through subsequent days.
3. Selection of genetic algorithm parameters:
- Population size: 200.
- Chromosome length: 144 (maximum number of blocks in a given day).
- Number of generations: 250 + 25 * the number of unique psychologists on that day.
- Gene space (number of possible values a gene can take):
- Number of solutions chosen as parents in each generation: 20.
    - A value of 0 indicates that the time block is empty.
    - A value in the form of a unique psychologist identifier indicates that the psychologist is selected during that time block.
- Mutation type: adaptive (mutates from 7 genes to 1 gene).
- Parent selection: steady-state selection.