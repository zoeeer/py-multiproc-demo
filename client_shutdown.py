from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass

if __name__ == '__main__':
    MyManager.register('shutdown')
    manager = MyManager(address=('localhost', 50000), authkey=b'abc')
    manager.connect()
    manager.shutdown()
