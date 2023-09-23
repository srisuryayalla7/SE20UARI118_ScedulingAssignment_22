from datetime import datetime

def time_to_minutes(time_str):
    # Convert HH:MM format time to minutes
    time_format = "%H:%M"
    time_obj = datetime.strptime(time_str.strip(), time_format)
    return time_obj.hour * 60 + time_obj.minute

def first_come_first_serve(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0

    current_time = 0
    process_order = []

    for i in range(num):
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        current_process = min(ready_processes, key=lambda x: x[1])
        process_order.append(current_process[0])

        process_id, arrival_time, burst_time, priority = current_process
        s_time = max(current_time, arrival_time)
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(current_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def shortest_job_first(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0

    current_time = 0
    process_order = []

    while processes:
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        shortest_process = min(ready_processes, key=lambda x: x[2])
        process_order.append(shortest_process[0])

        process_id, arrival_time, burst_time, priority = shortest_process
        s_time = current_time
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(shortest_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def priority_scheduling(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0

    current_time = 0
    process_order = []

    while processes:
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        highest_priority_process = min(ready_processes, key=lambda x: x[3])
        process_order.append(highest_priority_process[0])

        process_id, arrival_time, burst_time, priority = highest_priority_process
        s_time = current_time
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(highest_priority_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def round_robin(processes, time_quantum):
    num = len(processes)

    timer = 0
    avg_waiting_time = 0
    avg_turnaround_time = 0
    process_order = []

    tq = time_quantum
    n = num
    arrival = [0] * n
    burst = [0] * n
    wait = [0] * n
    turn = [0] * n
    temp_burst = [0] * n
    complete = [False] * n

    for i in range(n):
        arrival[i] = processes[i][1]

    for i in range(n):
        burst[i] = processes[i][2]
        temp_burst[i] = burst[i]

    while True:
        done = True
        for i in range(n):
            if temp_burst[i] > 0:
                done = False
                if temp_burst[i] > tq:
                    timer += tq
                    temp_burst[i] -= tq
                else:
                    timer += temp_burst[i]
                    wait[i] = timer - arrival[i] - burst[i]
                    temp_burst[i] = 0
                    turn[i] = timer - arrival[i]
                    complete[i] = True
                    process_order.append(f'P{i+1}')
        if done:
            break

    avg_waiting_time = sum(wait) / n
    avg_turnaround_time = sum(turn) / n

    return process_order, avg_waiting_time, avg_turnaround_time

if __name__ == "__main__":
    # Input processes: [["P1", "00:00", 30, 3], ["P2", "00:10", 20, 1], ["P3", "00:15", 40, 4], ["P4", "00:20", 15, 2]]
    processes = [["P1", "00:00", 30, 3], ["P2", "00:10", 20, 1], ["P3", "00:15", 40, 4], ["P4", "00:20", 15, 2]]

    # Convert arrival times to minutes
    for process in processes:
        process[1] = time_to_minutes(process[1])

    algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]

    results = {}  # Store results for each algorithm

    for algorithm in algorithms:
        if algorithm == "FCFS":
            process_order, avg_waiting_time, avg_turnaround_time = first_come_first_serve(processes.copy())
        elif algorithm == "SJF":
            process_order, avg_waiting_time, avg_turnaround_time = shortest_job_first(processes.copy())
        elif algorithm == "Priority":
            process_order, avg_waiting_time, avg_turnaround_time = priority_scheduling(processes.copy())
        elif algorithm == "Round Robin":
            time_quantum = 4  # Replace with your desired time quantum
            process_order, avg_waiting_time, avg_turnaround_time = round_robin(processes.copy(), time_quantum)

        results[algorithm] = (avg_waiting_time, avg_turnaround_time, process_order)

    # Print results for all algorithms
    for algorithm, (avg_waiting_time, avg_turnaround_time, process_order) in results.items():
        print(f"{algorithm}:")
        print(f"Process Order: {' -> '.join(process_order)}")
        print(f"Average Waiting Time: {avg_waiting_time}")
        print(f"Average Turnaround Time: {avg_turnaround_time}")
        print()

    # Select the best algorithm based on average waiting and turnaround time
    best_algorithm = min(results, key=lambda k: (results[k][0], results[k][1]))
    print(f"The best algorithm is: {best_algorithm}")

