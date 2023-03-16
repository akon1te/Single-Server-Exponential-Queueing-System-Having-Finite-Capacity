from model import Model
import matplotlib.pyplot as plt
import numpy as np
import pickle


MAX_CAPACITY = 20
LAMBDA = 2
MU = 1
SIZE = 10000
PATH = "dumps"


def test_P():
    
    pn = lambda i: (((LAMBDA/MU)**i) * (1 - LAMBDA/MU)) / (1 - (LAMBDA/MU)**(MAX_CAPACITY + 1))
    P = [pn(i) for i in range(MAX_CAPACITY)]
    
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)
    

def test_L():
    
    L = (LAMBDA*(1 + MAX_CAPACITY*(LAMBDA/MU)**(MAX_CAPACITY+1) - (MAX_CAPACITY + 1)*(LAMBDA/MU)**MAX_CAPACITY)) / ((MU - LAMBDA)*(1 - (LAMBDA/MU)**(MAX_CAPACITY+1)))
 
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)

    print(L, np.mean(queue))
    
    

if __name__ == "__main__":
    model = Model(max_queue_capacity=MAX_CAPACITY)
    model.generator(l=LAMBDA, mu=MU, size=SIZE)
    model.run()
    model.save(PATH)
    test_L()
    