import socket
import threading
import sys


def receive_messages(client_socket):
    """持续接收服务器消息的线程函数"""
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'), end='')
    except:
        pass
    finally:
        client_socket.close()
        print("\n连接已断开")
        sys.exit(0)


def start_client(host='localhost', port=8000):
    """启动聊天客户端"""
    # 创建套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接服务器
        client_socket.connect((host, port))
        print(f"已连接到聊天服务器 {host}:{port}")
        print("输入消息开始聊天,输入 'quit' 退出\n")

        # 启动接收消息的线程
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        )
        receive_thread.start()

        # 主线程负责发送消息
        while True:
            message = input()

            if message.lower() in ['quit', 'exit']:
                break

            if message:
                client_socket.sendall(message.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"错误: 无法连接到服务器 {host}:{port}")
        print("请确保服务器正在运行!")

    except Exception as e:
        print(f"发生错误: {e}")

    finally:
        client_socket.close()


if __name__ == '__main__':
    start_client()
