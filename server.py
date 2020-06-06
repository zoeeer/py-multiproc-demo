from multiprocessing import Process, Manager, Queue, Value, Event
from multiprocessing.managers import BaseManager
import os
import random
import signal
import time
import queue

class SendDataProcess(Process):
    def __init__(self):
        super().__init__(name='SendDataProcess')
        self.consumer = None
        self.queue = Queue(5)
        self.shutdown_event = Event()

    def run(self):
        print('starting sender', os.getpid())
        self.consumer = ConsumeDataProcess(self.shutdown_event, self.queue)
        self.consumer.start()
        i = 0
        while not self.shutdown_event.is_set():
            try:
                # 随机延迟0.5-1.5秒产生一个数据
                delay = random.randint(5, 15) / 10
                time.sleep(delay)
                self.consumer.queue.put(delay)
                i += 1
            except KeyboardInterrupt:
                print('SIGINT in sender process')
                break
        self.shutdown()

    def put_data(self, x):
        self.queue.put(x)

    def get_data(self):
        return self.queue.get()

    def shutdown(self):
        print('consumer: ', self.consumer)
        self.shutdown_event.set()
        if self.consumer:
            print('wait for consumer to stop')
            self.consumer.join()

    def terminate(self):
        print('terminating sender')
        self.shutdown()
        return super().terminate()

class ConsumeDataProcess(Process):
    def __init__(self, stop_flag, queue):
        super().__init__(name='ConsumeDataProcess')
        self.queue = queue
        self.stop_flag = stop_flag

    def run(self):
        print('starting consumer', os.getpid())
        while not self.stop_flag.is_set():
            try:
                # 随机延迟0.5-1.5秒取一次数据
                delay = random.randint(5, 15) / 10
                time.sleep(delay)
                data = self.queue.get(timeout=0.1)
                print(data)
            except queue.Empty:
                print('no data')
                continue
            except KeyboardInterrupt:
                print('SIGINT in consumer process')


class MyManager(BaseManager): pass

if __name__ == '__main__':
    print('starting main', os.getpid(), os.getppid())
    sender = SendDataProcess()
    sender.start()

    MyManager.register('get_sender_process', lambda: sender)
    manager = MyManager(address=('', 50000), authkey=b'abc')
    s = manager.get_server()
    print('starting process manager at {}'.format(manager.address))

    ### expose server shutdown call for clients
    import threading
    stop_timer = threading.Timer(1, lambda:s.stop_event.set())
    MyManager.register('shutdown', callable=lambda:stop_timer.start())

    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print('SIGINT in main')
    finally:
        if sender.is_alive():
            sender.terminate()
