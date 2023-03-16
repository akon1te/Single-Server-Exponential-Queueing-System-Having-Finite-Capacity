from model import Model
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import pickle


MAX_CAPACITY = 50
LAMBDA = 2
MU = 1
SIZE = 10000
PATH = "dumps"


def test_P():
    
    pn = lambda i: (((LAMBDA/MU)**i) * (1 - LAMBDA/MU)) / (1 - (LAMBDA/MU)**(MAX_CAPACITY + 1))
    P = np.array([pn(i) for i in range(MAX_CAPACITY + 1)])
    
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)
    
    total_time = time[-1]
    states_time = np.array([0] * (MAX_CAPACITY + 1), dtype=float)
    
    for i in range(len(time) - 1):
        states_time[queue[i]] += (time[i + 1] - time[i])
    states_time /= total_time

    print(f"Test P")
    print(P)
    print(states_time)
    #print(np.abs(P - states_time))  
    
    fig, ax = plt.subplots()
    ax.plot(range(MAX_CAPACITY + 1), states_time)
    ax.plot(range(MAX_CAPACITY + 1), P)
    plt.show()     
    
    

def test_L():
    
    L = (LAMBDA*(1 + MAX_CAPACITY*(LAMBDA/MU)**(MAX_CAPACITY+1) - (MAX_CAPACITY + 1)*(LAMBDA/MU)**MAX_CAPACITY)) / ((MU - LAMBDA)*(1 - (LAMBDA/MU)**(MAX_CAPACITY+1)))
 
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)

    print(f"Test L: {L}, {np.mean(queue)}")
    
    

if __name__ == "__main__":
    model = Model(max_queue_capacity=MAX_CAPACITY)
    model.generator(l=LAMBDA, mu=MU, size=SIZE)
    model.run()
    model.save(PATH)
    test_L()
    test_P()
    