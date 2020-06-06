from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass

if __name__ == '__main__':
    MyManager.register('get_sender_process')
    manager = MyManager(address=('localhost', 50000), authkey=b'abc')
    manager.connect()
    sender = manager.get_sender_process()
    print(sender.get_data())
    sender.put_data(99)
