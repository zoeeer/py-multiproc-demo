from multiprocessing.managers import BaseManager
import time

class MyManager(BaseManager): pass

if __name__ == '__main__':
    MyManager.register('get_sender_process')
    MyManager.register('shutdown')

    manager = MyManager(address=('localhost', 50000), authkey=b'abc')
    manager.connect()
    sender = manager.get_sender_process()

    # 读数据
    print('get data')
    print(sender.get_data())
    time.sleep(1)

    # 写数据
    print('put data')
    sender.put_data(3.14159)
    time.sleep(2)

    # 终止sender进程
    print('terminate sender')
    if sender.is_alive():
        sender.terminate()
    time.sleep(2)

    # 关闭manager
    print('shutdown server')
    manager.shutdown()
