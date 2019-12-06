import numpy as numpy
from numpy.random import rand, RandomState
import os
import time

SIMULATION_TIME = 60
poisson_arrival = [5, 5, 5, 5, 7, 8, 17, 25, 30, 23, 20, 18]


file_name = 'SIM_RESULT.csv'
if (os.path.exists(file_name)):
    os.remove(file_name)
write_file = open(file_name, 'a')
write_file.write('interval,number_of_buses,total_passengers_served,total_passengers_lost,revenue_gained,revenue_lost,total_wait_time,average_wait_time,program_execution_time\n')

for interval_count in range(4):
    for do_while in range(100):
        start_time = time.time()
        stop_details = []
        rand_generator = RandomState()

        def gen_time(multiplicator, num):
            return ((multiplicator - 1) * 10) + num

        for stop in range(1, 6):
            total_arrival_time = []
            for time_idx in range(len(poisson_arrival)):
                lam = poisson_arrival[time_idx]
                num_passenger = int(rand_generator.poisson(
                    lam * SIMULATION_TIME) / 5)
                passenger_arrival_time = numpy.sort(
                    rand(num_passenger) * SIMULATION_TIME)
                for i in range(len(passenger_arrival_time)):
                    passenger_arrival_time[i] += (time_idx * 60)
                total_arrival_time.extend(passenger_arrival_time)
            stop_details.append(total_arrival_time)

        # at this point, we have list of all queues across all stop
        # now start bus journey
        START_TIME = 5
        LAST_BUS_TIME = 715
        CURR_BUS_INTERVAL = 20 - (interval_count * 5)
        INTERVAL_BETWEEN_STOPS = 10
        BUS_CAPACITY = 50

        curr_bus_start_time = START_TIME
        total_bus_num = 0
        passengers_ride = 0
        # passengers_lost = 0
        total_wait_time = 0
        total_passengers_in_queue = 0

        while curr_bus_start_time < LAST_BUS_TIME:
            total_bus_num += 1
            curr_time = curr_bus_start_time
            num_passenger_bus = 0
            curr_time += INTERVAL_BETWEEN_STOPS
            for stop in stop_details:
                idx = 0
                if (num_passenger_bus >= BUS_CAPACITY):
                    idx = len(stop)
                while idx < len(stop):
                    arr_time = stop[idx]
                    if arr_time < curr_time:
                        total_passengers_in_queue += 1
                        if num_passenger_bus < BUS_CAPACITY:
                            if curr_time - arr_time <= 20:
                                total_wait_time += (curr_time - arr_time)
                                passengers_ride += 1
                                num_passenger_bus += 1
                            # else:
                            #     passengers_lost += 1
                            stop.remove(arr_time)
                            idx -= 1
                    idx += 1
            curr_bus_start_time += CURR_BUS_INTERVAL

        for stop in stop_details:
            total_passengers_in_queue += len(stop)

        passengers_lost = total_passengers_in_queue-passengers_ride

        write_file.write(f'{CURR_BUS_INTERVAL},{total_bus_num},{passengers_ride},{passengers_lost},{passengers_ride * 3},{passengers_lost * 3},{round(total_wait_time,2)},{round(total_wait_time/passengers_ride,2)},{time.time() - start_time}\n')
