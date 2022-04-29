import time
from itertools import count
from multiprocessing import Process
def inc_forever():
    print('Starting function inc_forever()...')
    while True:
        time.sleep(1)
        print(next(counter))
def return_zero():
    print('Starting function return_zero()...')
    return 0
if __name__ == '__main__':
    # counter is an infinite iterator
    counter = count(0)
    p1 = Process(target=inc_forever, name='Process_inc_forever')
    p2 = Process(target=return_zero, name='Process_return_zero')
    p1.start()
    p2.start()
    p1.join(timeout=5)
    p2.join(timeout=5)
    p1.terminate()
    p2.terminate()
if p1.exitcode is None:
       print(f'Oops, {p1} timeouts!')
if p2.exitcode == 0:
        print(f'{p2} is luck and finishes in 5 seconds!')
