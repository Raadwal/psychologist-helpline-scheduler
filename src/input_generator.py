import random

week_days = ['pn', 'wt', 'sr', 'cz', 'pt', 'sb', 'nd']
names = ['Anna', 'Jan', 'Wojtek', 'Adam', 'Joanna', 'Andrzej', 'Rafal', 'Tomasz', 'Sebastian', 'Daniel', 'Maciej', 'Grzegorz', 'Julia', 'Malgorzata']
descriptions = ['TAK', 'EWENT', 'NIE']
file_size = 250

def random_time():
    start_hour = random.randint(0, 22)
    end_hour = random.randint(start_hour + 1, min(start_hour + 3, 23))
    minute = random.choice([0, 10, 20, 30, 40, 50])
    return f'{start_hour:02d}:{minute:02d}', f'{end_hour:02d}:{minute:02d}'

data = []
for _ in range(file_size):
    name = random.choice(names)
    day = random.choice(week_days)
    start_time, end_time = random_time()
    description = random.choice(descriptions)
    data.append(f'{name} {day} {start_time}-{end_time} {description}')

with open('dostepnosc.txt', 'w') as file:
    file.write('\n'.join(data))