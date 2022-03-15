from multiprocessing import Process, Value


class Multi:
    def __init__(self):
        self.x = Value('i', 20)

    def loop(self):
        for i in range(1, 100):
            self.x.value = i


if __name__ == '__main__':
    M = Multi()
    p = Process(target=M.loop)
    p.start()
    p.join()

    print(int(M.x.value))