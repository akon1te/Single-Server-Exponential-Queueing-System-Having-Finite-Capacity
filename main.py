from model import Model
import matplotlib.pyplot as plt
import numpy as np
import pickle


MAX_CAPACITY = 20
LAMBDA = 2
MU = 1
SIZE = 100000
PATH = "dumps"


def load_dumps():
    with open(f'{PATH}/time.pkl', 'rb') as tf:
        time = pickle.load(tf)
    with open(f'{PATH}/queue_size.pkl', 'rb') as qf:
        queue_size = pickle.load(qf)
    with open(f'{PATH}/queue_state.pkl', 'rb') as qf:
        queue_state = pickle.load(qf)
    with open(f'{PATH}/server.pkl', 'rb') as sf:
        server = pickle.load(sf)

    return time, queue_size, queue_state, server


def test_P():
    pn = lambda i: (((LAMBDA/MU)**i) * (1 - LAMBDA/MU)) / (1 - (LAMBDA/MU)**(MAX_CAPACITY + 1))
    P = np.array([pn(i) for i in range(MAX_CAPACITY + 1)])
    
    time, queue, _, _ = load_dumps()
    
    total_time = time[-1]
    states_time = np.array([0] * (MAX_CAPACITY + 1), dtype=float)
    
    for i in range(len(time) - 1):
        states_time[queue[i]] += (time[i + 1] - time[i])
    states_time /= total_time
    
    fig, ax = plt.subplots()
    plt.title('Стационарное распределение')
    ax.bar(range(MAX_CAPACITY + 1), states_time, alpha=0.5, label='Экспериментальное')
    ax.bar(range(MAX_CAPACITY + 1), P, alpha=0.5, label='Теоритическое')
    plt.legend()
    plt.show()     
    

def test_L():
    
    L = (LAMBDA*(1 + MAX_CAPACITY*(LAMBDA/MU)**(MAX_CAPACITY+1) - (MAX_CAPACITY + 1)*(LAMBDA/MU)**MAX_CAPACITY)) / ((MU - LAMBDA)*(1 - (LAMBDA/MU)**(MAX_CAPACITY+1)))
 
    _, queue, _, _ = load_dumps()

    print(f"Test L: {L} - {np.mean(queue)}")
    

def test_W():

    pn = lambda i: (((LAMBDA/MU)**i) * (1 - LAMBDA/MU)) / (1 - (LAMBDA/MU)**(MAX_CAPACITY + 1))
    P = np.array([pn(i) for i in range(MAX_CAPACITY + 1)])
    L = (LAMBDA*(1 + MAX_CAPACITY*(LAMBDA/MU)**(MAX_CAPACITY+1) - (MAX_CAPACITY + 1)*(LAMBDA/MU)**MAX_CAPACITY)) / ((MU - LAMBDA)*(1 - (LAMBDA/MU)**(MAX_CAPACITY+1)))
 
    time, _, queue_state, server = load_dumps()    
    waiting_times = []     
    
    for i in range(len(time)):
        waiting_times.append(server[i] + np.sum(queue_state[i]))

    waiting_times = np.cumsum(waiting_times) / np.array(list(range(1, len(time) + 1)))

    lambda_a = LAMBDA * (1 - P[-1])
    W = L / lambda_a

    fig, ax = plt.subplots()
    plt.title('Среднее время ожидания')
    ax.plot(range(len(time)), waiting_times, alpha=0.5, label='Экспериментальное')
    ax.axhline(y=W, color='k', linestyle='--', label='Теоритическое')
    plt.legend()
    plt.show()    

    print(f"Test W: {W} - {waiting_times[-1]}")
    

if __name__ == "__main__":
    model = Model(max_queue_capacity=MAX_CAPACITY)
    model.generator(l=LAMBDA, mu=MU, size=SIZE)
    model.run()
    model.save(PATH)

    #test_L()
    #test_P()
    test_W()
    