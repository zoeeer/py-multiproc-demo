# Python multiprocessing demo

This is a simple demo to start with on python multiprocess programming.

## Demo 说明

运行server.py会启动3个进程：
1. 主进程
   - 管理其他进程
   - 启动进程Manager服务程序，监听客户端
2. sender进程（SendDataProcess）
   - 数据生产者（每隔1秒左右发送一个数据到队列）
   - 管理consumer进程
3. consumer进程（ConsumeDataProcess）
   - 数据消费者（每隔1秒左右从队列取出一个数据）

运行client.py会连接服务端并执行若干操作：
1. 获取服务端的sender对象
2. 从sender的队列中读取数据
3. 往sender的队列中写入数据
4. 调用sender.terminate()方法，终止sender进程（由sender终止consumer进程）
5. 调用服务端注册的shutdown()方法，关闭服务程序

## 代码文件
- server.py 主程序
- client.py 客户端：连接manager，读写sender数据、关闭sender、关闭manager
- client_putdata.py  客户端：读写sender数据
- client_shutdown.py 客户端：关闭manager

## 运行Demo (Python 3.5+)
```
python server.py           # 启动server
python client_putdata.py   # 跨进程读写数据
python client_shutdown.py  # 跨进程关闭server

python server.py  # 启动server
python client.py  # 跨进程读写和关闭
```
