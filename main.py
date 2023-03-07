from model import Model

MAX_CAPACITY = 10
L = 2
MU = 1
SIZE = 100


if __name__ == "__main__":

    model = Model(max_queue_capacity=MAX_CAPACITY)
    model.generator(l=L, mu=MU, size=SIZE)
    model.run()
    model.save("dumps")
