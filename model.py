import numpy as np
import logging
import os
import pickle
from typing import Union

logging.basicConfig(filename=f'queue_state.log',
                    filemode='w', format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Model():

    def __init__(self, max_queue_capacity: int, conditions: Union[list, None] = None):

        self.max_queue_capacity = max_queue_capacity
        self.conditions = conditions
        self.time_log = []
        self.queue_state_log = []
        self.queue_size_log = []
        self.server_log = []


    def generator(self, l: int, mu: int, size: int):
        self.conditions = [[np.random.exponential(
            scale=1/l, size=1)[0], np.random.exponential(1/mu, size=1)[0]] for _ in range(size)]


    def run(self):

        assert len(self.conditions) > 0

        current_time = 0
        remaining_server_time = 0
        current_queue_occupancy = []

        while len(self.conditions) != 0:

            t1, t2 = self.conditions.pop(0)
            logger.info(f"Current itteration t1: {t1} - t2: {t2}")
            logger.info(
                f"Before itter. Server state: {remaining_server_time}, Queue state: {current_queue_occupancy}")

            #If time before next requests greater than processing time of the request on server and requests in the queue
            if t1 >= sum(current_queue_occupancy) + remaining_server_time:
                while len(current_queue_occupancy) != 0 and t1 > 0:

                    t1 -= remaining_server_time
                    current_time += remaining_server_time
                    remaining_server_time = 0
                    if len(current_queue_occupancy) != 0:
                        remaining_server_time = current_queue_occupancy.pop(0)

                    self.dump(current_time, current_queue_occupancy,
                                remaining_server_time)

                #Adding new request on server
                current_time += t1
                remaining_server_time = t2

                self.dump(current_time, current_queue_occupancy,
                                remaining_server_time)

            else:

                #If time before next requests lesser than processing time of the request on server
                if remaining_server_time > t1:
                    remaining_server_time -= t1
                    current_time += t1

                    if len(current_queue_occupancy) == self.max_queue_capacity:
                        logger.info(f"Queue is full. Drop this operations.\n")
                    else:
                        current_queue_occupancy.append(t2)

                    self.dump(current_time, current_queue_occupancy,
                              remaining_server_time)

                #If time before next requests leeser than processing time of the request on server and requests in the queue
                else:

                    while len(current_queue_occupancy) != 0 and t1 != 0:

                        if t1 > remaining_server_time:
                            t1 -= remaining_server_time
                            current_time += remaining_server_time
                            if len(current_queue_occupancy) != 0:
                                remaining_server_time = current_queue_occupancy.pop(0)

                            self.dump(current_time, current_queue_occupancy,
                                  remaining_server_time)
                        else:
                            remaining_server_time -= t1
                            current_time += t1
                            t1 = 0
                            current_queue_occupancy.append(t2)
                            self.dump(current_time, current_queue_occupancy,
                                remaining_server_time)

            logger.info(
                f"After itter. Server state: {remaining_server_time}, Queue state: {current_queue_occupancy}\n")

        if remaining_server_time != 0 or len(current_queue_occupancy):
            current_time += remaining_server_time

            while len(current_queue_occupancy) != 0:

                remaining_server_time = current_queue_occupancy.pop(0)

                self.dump(current_time, current_queue_occupancy,
                remaining_server_time)

                current_time += remaining_server_time


    def dump(self, current_time: float, current_queue_occupancy: list, remaining_server_time: float):

        self.time_log.append(current_time)
        self.queue_state_log.append(current_queue_occupancy.copy())
        self.queue_size_log.append(len(current_queue_occupancy))
        self.server_log.append(remaining_server_time)


    def save(self, path: str):

        try:
            os.mkdir(path)
        except:
            pass


        with open(f'{path}/time.pkl', 'wb') as tf:
            pickle.dump(self.time_log, tf)
        with open(f'{path}/queue_size.pkl', 'wb') as qf:
            pickle.dump(self.queue_size_log, qf)
        with open(f'{path}/queue_state.pkl', 'wb') as qf:
            pickle.dump(self.queue_state_log, qf)
        with open(f'{path}/server.pkl', 'wb') as sf:
            pickle.dump(self.server_log, sf)