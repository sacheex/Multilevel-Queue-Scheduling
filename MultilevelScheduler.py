execute_time = 0
terminated = []
def proc_initialize(processes):
    for process in processes:
        process['remaining_time'] = process['burst_time']
        process['finish_time'] = 0
        process['waiting_time'] = 0
    return processes

def print_data(processes):
    for p in processes:
        print(p)

def FCFS_scheduler(processes, swap_time):
    global terminated, execute_time
    timer = swap_time

    while processes and timer > 0:
        
        for process in processes.copy():
            # print(f"PID = {process['pid']} / Wait = {process['waiting_time']} / Finish = {process['finish_time']} / Exc = {execute_time}")
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
            # print(f"Wait = {process['waiting_time']} / Finish = {process['finish_time']} / Exc = {execute_time}\n")

            if process['remaining_time'] == 0:
                proc_index = processes.index(process)
                terminated.append(processes.pop(proc_index))
                
            if all(process['remaining_time'] == 0 for process in processes) or timer <= 0:
                break

        if not processes:
            for process in terminated:
                process['turnaround_time'] = process['finish_time']
            # print_data(terminated)
            
def RoundRobin(processes, time_q, swap_time):
    timer = swap_time
    global terminated, execute_time
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
            # print_data(terminated)
            
processes1 = [
        {'pid' : 1, 'burst_time': 10},
        {'pid' : 2, 'burst_time': 12},
        {'pid' : 3, 'burst_time': 8},
    ]
processes2 = [
    {'pid' : 4, 'burst_time': 15},
    {'pid' : 5, 'burst_time': 13}
]
processes1 = proc_initialize(processes1)
processes2 = proc_initialize(processes2)
while processes1 or processes2:
    if processes1:
        FCFS_scheduler(processes1, 20)
    if processes2:
        RoundRobin(processes2, 5, 20)

print_data(terminated)


