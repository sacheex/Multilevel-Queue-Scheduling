class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.finish_time = []
        self.waiting_time = []
        self.current_time = 0
        self.turnaround_time = []
        self.total_waiting_time = 0
        self.total_turnaround_time = 0

    def get_arrival_time(self):
        return self.processes['arrival_time']
    
    def get_waiting_time(self):
        pass

    def print_data(self):
        for process in self.processes:
            self.total_turnaround_time += process['turnaround_time']
            self.total_waiting_time += process['waiting_time']
            
        print(f"--------- {self.__class__.__name__} ---------".center(70))
        print()
        print(f"{'Process ID':>10} | {'Arrival Time':>12} | {'Burst Time':>10} | {'Waiting Time':>12} | {'Turnaround Time':>15}")

        for process in self.processes:
            print(f"{process['pid']:>6}  {process['arrival_time']:>12}  {process['burst_time']:>10}  {process['waiting_time']:>12}  {process['turnaround_time']:>15}")

        print("Average waiting time = ", self.total_waiting_time / len(self.processes))
        print("Average turnaround time = ", self.total_turnaround_time / len(self.processes))
    
    
class FCFS(Scheduler):
    def __init__(self, processes):
        super().__init__(processes)
    
    def schedule(self):
        processes = sorted(self.processes, key = lambda x: x['arrival_time'])
        current_time = 0
        for process in processes:
            if current_time < process['arrival_time']:
                current_time = process['arrival_time']
            if current_time < process['arrival_time']:
                process['waiting_time'] = 0
            else:
                process['waiting_time'] = current_time - process['arrival_time']
            current_time += process['burst_time']
            process['turnaround_time'] = current_time 

class RoundRobin(Scheduler):
    def __init__(self, processes,time_q):
        super().__init__(processes)
        self.time_q = time_q

    def schedule(self):
        processes = sorted(self.processes, key = lambda x: x['arrival_time'])
        for process in processes:
            process['remaining_time'] = process['burst_time']
            process['turnaround_time'] = 0
            process['waiting_time'] = 0
        
        current_time = 0
        while any(process['remaining_time'] != 0 for process in processes):
            for process in processes:
                if process['remaining_time'] > 0:
                    if current_time < process['arrival_time']:
                        current_time = process['arrival_time'] 
                    if process['turnaround_time'] == 0 and current_time > process['arrival_time']:
                        process['waiting_time'] =current_time - process['arrival_time']
                    else:
                        process['waiting_time'] += current_time - process['turnaround_time']


                    if process['remaining_time'] >= self.time_q:
                        process['remaining_time'] -= self.time_q
                        current_time += self.time_q
                    else:
                        current_time += process['remaining_time']
                        process['remaining_time'] = 0
                    
                    process['turnaround_time'] = current_time
        
class ShortestJobFirst(Scheduler):
    def __init__(self, processes):
        super().__init__(processes)

    def schedule(self):
        processes = sorted(self.processes, key = lambda x: x['burst_time'])
        current_time = 0
        for process in processes:
            process['waiting_time'] = current_time
            current_time += process['burst_time']
            process['turnaround_time'] = current_time
    def print_data(self):
        for process in self.processes:
            self.total_turnaround_time += process['turnaround_time']
            self.total_waiting_time += process['waiting_time']
            
        print(f"--------- {self.__class__.__name__} ---------".center(70))
        print()
        print(f"{'Process ID':>10} | {'Burst Time':>10} | {'Waiting Time':>12} | {'Turnaround Time':>15}")

        for process in self.processes:
            print(f"{process['pid']:>6}   {process['burst_time']:>10}  {process['waiting_time']:>12}  {process['turnaround_time']:>15}")

        print("Average waiting time = ", self.total_waiting_time / len(self.processes))
        print("Average turnaround time = ", self.total_turnaround_time / len(self.processes))

processes = [
    {'pid' : 1, 'arrival_time': 0, 'burst_time': 10},
    {'pid' : 2, 'arrival_time': 2, 'burst_time': 7},
    {'pid' : 3, 'arrival_time': 4, 'burst_time': 3},
    {'pid' : 4, 'arrival_time': 9, 'burst_time': 5},
    {'pid' : 5, 'arrival_time': 6, 'burst_time': 4}
]

fcfs = FCFS(processes)

fcfs.schedule()
fcfs.print_data()

rr = RoundRobin(processes, 4)
rr.schedule()
rr.print_data()

sjf = ShortestJobFirst(processes)
sjf.schedule()
sjf.print_data()