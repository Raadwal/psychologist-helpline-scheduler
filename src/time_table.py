import numpy as np

class TimeBlock:
    def __init__(self, name, day, start_time, end_time, description):
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __str__(self):
        start_time_str = f'{self.start_time // 60:02d}:{self.start_time % 60:02d}'
        end_time_str = f'{self.end_time // 60:02d}:{self.end_time % 60:02d}'
        return f'{self.name} {self.day} {start_time_str}-{end_time_str} {self.description}'

class TimeTable:
    def __init__(self, file_path):
        self.week_days = ['pn', 'wt', 'sr', 'cz', 'pt', 'sb', 'nd']
        self.time_blocks = [[], [], [], [], [], [], []]
        self.unique_people = [{}, {}, {}, {}, {}, {}, {}]
    
        self._parse_file(file_path)

    def _parse_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 4: 
                    name, day, time, description = parts
                elif len(parts) == 3:
                    name, day, time = parts
                    description = ''
                else:
                    continue
                start_time_str, end_time_str = time.split('-')
                start_time = int(start_time_str.split(':')[0])*60 + int(start_time_str.split(':')[1])
                end_time = int(end_time_str.split(':')[0])*60 + int(end_time_str.split(':')[1])

                day_index = self.week_days.index(day)
                for time in range(start_time, end_time, 10):
                    time_block = TimeBlock(name, day, time, time + 10, description)
                    self.time_blocks[day_index].append(time_block)

                if name not in self.unique_people[day_index]:
                    self.unique_people[day_index][name] = len(self.unique_people[day_index]) + 1

    def get_days(self):
        return self.week_days

    def get_time_blocks(self, day):
        if day in self.week_days:
            day_index = self.week_days.index(day)
            return self.time_blocks[day_index]
        else:
            return None

    def get_unique_people(self, day):
        if day in self.week_days:
            day_index = self.week_days.index(day)
            return self.unique_people[day_index]
        else:
            return 
        
    def get_availability_arrays(self, day):
        if day in self.week_days:
            day_index = self.week_days.index(day)
            availability_arrays = {}
            for name, id in self.unique_people[day_index].items():
                availability_array = np.zeros(144) 
                for time_block in self.time_blocks[day_index]:
                    if time_block.name == name:
                        start_index = time_block.start_time // 10
                        end_index = time_block.end_time // 10
                        if time_block.description == 'TAK':
                            value = 1
                        elif time_block.description == 'EWENT':
                            value = 0.5
                        else:
                            value = -1
                        availability_array[start_index:end_index] = value
                availability_arrays[id] = availability_array
            return availability_arrays
        else:
            return None

    def save_to_file(self, solution, filename):
        with open(filename, 'w') as file:
            for day_index, day_solution in enumerate(solution):
                if day_solution is None:
                    continue

                day = self.week_days[day_index]
                availability_arrays = self.get_availability_arrays(day)
                
                id_to_name = {id: name for name, id in self.unique_people[day_index].items()}
                i = 0

                while i < len(day_solution[0]):
                    person_id = day_solution[0][i]
                    if person_id == 0:
                        i += 1
                        continue
                    
                    if(availability_arrays[person_id][i] <= 0):
                        i += 1
                        continue
                    
                    person_name = id_to_name[person_id]
                    start_time = i * 10

                    while i + 1 < len(day_solution[0]) and day_solution[0][i + 1] == person_id and availability_arrays[person_id][i + 1] > 0:
                        i += 1

                    end_time = (i + 1) * 10

                    start_time_str = f'{start_time // 60:02d}:{start_time % 60:02d}'
                    end_time_str = f'{end_time // 60:02d}:{end_time % 60:02d}'

                    file.write(f'{person_name} {day} {start_time_str}-{end_time_str}\n')

                    i += 1
                 