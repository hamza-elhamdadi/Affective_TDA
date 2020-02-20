import multiprocessing

def print_cube(num):
    for i in range(num):
        print('yellow')

def print_square(num):
    for i in range(num):
        print('red')

p1 = multiprocessing.Process(target=print_cube, args=(100000000000000, ))
p2 = multiprocessing.Process(target=print_square, args=(100000000000000, ))

p1.start()
p2.start()

p1.join()
p2.join()

