from model import Model
import matplotlib.pyplot as plt
import pickle

MAX_CAPACITY = 20
LAMBDA = 2
MU = 1
SIZE = 100
PATH = "dumps"


def test_P():
    
    pn = lambda i: (((LAMBDA/MU)**i) * (1 - LAMBDA/MU)) / (1 - (LAMBDA/MU)**(SIZE + 1))
    P = [pn(i) for i in range(SIZE)]
    
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)
    

def test_L():
        
    L = (LAMBDA*(1 + SIZE*(LAMBDA/MU)**(SIZE+1) - (SIZE + 1)*(LAMBDA/MU)**SIZE)) / ((MU - LAMBDA)*(1 - (LAMBDA/MU)**SIZE+1))
 
    with open(f'{PATH}/queue.pkl', 'rb') as qf:
        queue = pickle.load(qf) 
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)
    
    

if __name__ == "__main__":

    model = Model(max_queue_capacity=MAX_CAPACITY)
    model.generator(l=LAMBDA, mu=MU, size=SIZE)
    model.run()
    #model.save(PATH)
    