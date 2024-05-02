execute_time = 0 # Keep track of the execution time of the program
terminated = [] # Hold terminated processes


def proc_initialize(processes):
    '''
    Initialize processes with default values
    '''
    for process in processes:
        process['remaining_time'] = process['burst_time']
        process['finish_time'] = 0
        process['waiting_time'] = 0
    return processes

def print_data(processes):
    '''
    Print data to the terminal
    '''
    print()

    total_waiting = 0
    total_turnaround = 0
    processes.sort(key = lambda x: x['pid'])

    for process in processes:
        total_turnaround += process['turnaround_time']
        total_waiting += process['waiting_time']

    # Print process data in a table
    print(f"{'*' * 30} MULTILEVEL QUEUE {'*' * 30}".center(70))
    print()
    print('=' * 70)
    print(f"{'Process ID':>10} | {'Burst Time':>10} | {'Waiting Time':>12} | {'Turnaround Time':>15}")
    print('=' * 70)

    for process in processes:
        print(f"{process['pid']:>8}   {process['burst_time']:>10}   {process['waiting_time']:>12}   {process['turnaround_time']:>15}")
        print('-' * 70)

    # Total waiting and Turnaround time
    print(f"Average waiting time = {total_waiting / len(processes):.2f}")
    print(f"Average turnaround time = {total_turnaround / len(processes):.2f}")
    print('=' * 70)


def FIFO(processes, swap_time):
    '''
    First IN First Out Algorithm
    '''
    global terminated, execute_time
    timer = swap_time

    while processes and timer > 0:
        
        for process in processes.copy():
            process['waiting_time'] += execute_time - process['finish_time']

            if timer >= process['remaining_time']:
                timer -= process['remaining_time']
                execute_time += process['remaining_time']
                process['remaining_time'] = 0

            elif process['remaining_time'] > timer:
                process['remaining_time'] -= timer
                execute_time += timer
                timer = 0

            process['finish_time'] = execute_time

            if process['remaining_time'] == 0:
                proc_index = processes.index(process)
                terminated.append(processes.pop(proc_index))
                
            if all(process['remaining_time'] == 0 for process in processes) or timer <= 0:
                break

        if not processes:
            for process in terminated:
                process['turnaround_time'] = process['finish_time']


def RoundRobin(processes, time_q, swap_time):
    '''
    Round Robin Algorithm
    '''
    timer = swap_time
    global terminated, execute_time
    rr_waiting = 0
    rr_turnaround = 0
    while processes and timer > 0:
        
        for process in processes.copy():

            process['waiting_time'] += execute_time - process['finish_time']

            if timer > time_q:
                if process['remaining_time'] > time_q:
                    process['remaining_time'] -= time_q
                    timer -= time_q
                    execute_time += time_q
                else:
                    timer -= process['remaining_time']
                    execute_time += process['remaining_time']
                    process['remaining_time'] = 0
                
            else:
                if process['remaining_time']  > timer:
                    process['remaining_time']  -= timer
                    execute_time += timer
                    timer = 0
                
                else:
                    timer -= process['remaining_time'] 
                    execute_time += process['remaining_time'] 
                    process['remaining_time'] = 0

            process['finish_time'] = execute_time
            if process['remaining_time'] == 0:
                proc_index = processes.index(process)
                terminated.append(processes.pop(proc_index))
                
            if all(process['remaining_time'] == 0 for process in processes) or timer <= 0:
                break

        if not processes:
            for process in terminated:
                process['turnaround_time'] = process['finish_time']


def SJF(processes, swap_time):
    '''
    Shortest Job First Algorithm
    '''
    global terminated, execute_time
    timer = swap_time
    processes.sort(key = lambda x: x['burst_time'])
    while processes and timer > 0:
        
        for process in processes.copy():

            process['waiting_time'] += execute_time - process['finish_time']

            if timer >= process['remaining_time']:
                timer -= process['remaining_time']
                execute_time += process['remaining_time']
                process['remaining_time'] = 0

            elif process['remaining_time'] > timer:
                process['remaining_time'] -= timer
                execute_time += timer
                timer = 0

            process['finish_time'] = execute_time

            if process['remaining_time'] == 0:
                proc_index = processes.index(process)
                terminated.append(processes.pop(proc_index))
                
            if all(process['remaining_time'] == 0 for process in processes) or timer == 0:
                break

        if not processes:
            for process in terminated:
                process['turnaround_time'] = process['finish_time']


def multilevel_scheduler(processes, swap_time, time_q =0):
    # Initialize each processes lists with default value
    q0 = proc_initialize(processes[0])
    q1 = proc_initialize(processes[1])
    q2 = proc_initialize(processes[2])
    q3 = proc_initialize(processes[3])

    # Run each scheduling algorithm until every process get terminated
    while q0 or q1 or q2 or q3:
        if q0:
            RoundRobin(q0, time_q, swap_time)
        if q1:
            SJF(q1, swap_time)
        if q2:
            SJF(q2, swap_time)
        if q3:
            FIFO(q3, swap_time)
    print_data(terminated)
        

if __name__ == "__main__":

    count = 0
    processes = [[], [], [], []] # 2-D list to hold processes with four priorities

    while True:
        
        # Header
        print(''' 
              ###########################
              ## MULTILEVEL SCHEDULING ##
      ________###########################________
            
    Options:
        1. Add processes to queue
        2. Run the scheduler
        3. Run with Demo data
        4. Exit
        ''')
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            print('''
                ** Add Process to Queue **
                  ''')
            no_of_proc, priority = map(int, input("Enter number of processes and their priority[0-high, 3-low] seperated by space: ").split())
            
            if priority == 0:
                time_q = int(input("Enter time quantum for Round Robin: "))

            for i in range(no_of_proc):
                burst_t = int(input(f"Enter Burst time for process {i + 1}: "))
                count += 1
                processes[priority].append({'pid': count, "burst_time": burst_t})

        elif choice == 2:
            '''
            Run Multilevel scheduler
            '''
            multilevel_scheduler(processes, 20, time_q)
        
        elif choice == 3:
            '''
            Run the program with predefined data
            '''
            processes = [
                [
                    {'pid' : 1, 'burst_time': 10},
                    {'pid' : 2, 'burst_time': 12}
                ],
                [
                    {'pid' : 3, 'burst_time': 8},
                    {'pid' : 4, 'burst_time': 15}
                ],

                [
                    {'pid' : 5, 'burst_time': 13},
                    {'pid' : 6, 'burst_time': 15}
                ],

                [
                    {'pid' : 7, 'burst_time': 7},
                    {'pid' : 8, 'burst_time': 10},
                    {'pid' : 9, 'burst_time': 13}
                ]
            ]
            
            multilevel_scheduler(processes, 20, 5)

        elif choice == 4:
            '''
            Exit from the program
            '''
            print("Bye!")
            break

        else:
            print("Invalid choice! Try again.")
