import socket
import threading
from datetime import datetime


class ChatServer:
    """聊天服务器类"""

    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # 存储客户端信息 {client_socket: address}
        self.lock = threading.Lock()  # 用于保护共享资源

    def broadcast(self, message, sender_socket=None):
        """广播消息给所有连接的客户端"""
        with self.lock:
            for client_socket in list(self.clients.keys()):
                # 不发送给发送者自己(可选)
                if sender_socket and client_socket == sender_socket:
                    continue

                try:
                    client_socket.sendall(message.encode('utf-8'))
                except:
                    # 如果发送失败,移除该客户端
                    self.remove_client(client_socket)

    def remove_client(self, client_socket):
        """移除客户端"""
        with self.lock:
            if client_socket in self.clients:
                address = self.clients[client_socket]
                del self.clients[client_socket]
                client_socket.close()
                print(f"[离线] {address} 已断开连接")

    def handle_client(self, client_socket, client_address):
        """处理单个客户端连接"""
        print(f"[新连接] {client_address} 已连接")

        # 将客户端添加到列表
        with self.lock:
            self.clients[client_socket] = client_address

        # 发送欢迎消息
        welcome_msg = f"欢迎加入聊天室! 当前在线人数: {len(self.clients)}\n"
        client_socket.sendall(welcome_msg.encode('utf-8'))

        # 通知其他人有新用户加入
        join_msg = f"\n[{datetime.now().strftime('%H:%M:%S')}] {client_address} 加入了聊天室\n"
        self.broadcast(join_msg, sender_socket=client_socket)

        try:
            while True:
                # 接收消息
                message = client_socket.recv(1024)

                if not message:
                    break

                # 解码消息
                decoded_message = message.decode('utf-8').strip()

                if not decoded_message:
                    continue

                # 格式化消息
                formatted_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {client_address}: {decoded_message}\n"

                # 显示在服务器控制台
                print(formatted_msg.strip())

                # 广播给所有客户端
                self.broadcast(formatted_msg)

        except ConnectionResetError:
            print(f"[断开连接] {client_address} 异常断开")

        finally:
            # 清理客户端
            leave_msg = f"\n[{datetime.now().strftime('%H:%M:%S')}] {client_address} 离开了聊天室\n"
            self.remove_client(client_socket)
            self.broadcast(leave_msg)

    def start(self):
        """启动服务器"""
        # 创建套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定和监听
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print("=" * 50)
        print(f"群聊服务器已启动")
        print(f"监听地址: {self.host}:{self.port}")
        print("等待客户端连接...")
        print("=" * 50)

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()

                # 创建线程处理客户端
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\n服务器正在关闭...")

        finally:
            self.server_socket.close()
            print("服务器已关闭")


if __name__ == '__main__':
    server = ChatServer()
    server.start()
