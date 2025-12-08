import network
import time
import socket
import request_parser
import errno


# ==================== 网络层 ====================
def connect_wifi(wifi_ssid: str, wifi_pwd: str) -> network.WLAN:
    """纯网络功能：连接Wi-Fi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"[网络] 正在连接至 {wifi_ssid}...")
        wlan.connect(wifi_ssid, wifi_pwd)
        while not wlan.isconnected():
            time.sleep_ms(200)
    ip_addr = wlan.ifconfig()[0]
    print(f"[网络] 连接成功! IP: {ip_addr}")
    return wlan


def start_server(
    wlan: network.WLAN, controller: BaseController, server_port: int = 8080
) -> None:
    """纯网络功能：启动TCP服务器"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", server_port))
    server_socket.listen(5)

    ip_addr = wlan.ifconfig()[0]
    print(f"[网络] 服务器启动在 {ip_addr}:{server_port}")
    print("[网络] 等待客户端连接...")
    print("=" * 50)

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            # 处理客户端请求并发送响应
            handle_client_request(client_socket, client_addr, wlan, controller)
        except KeyboardInterrupt:
            print("\n[网络] 服务器关闭")
            server_socket.close()
            break
        except Exception as e:
            print(f"[错误] 服务器主循环: {e}")


def handle_client_request(
    client_socket: socket.socket,
    client_addr: Tuple[str, int],
    wlan: network.WLAN,
    controller: BaseController,
) -> None:
    """处理单个客户端请求并发送响应"""
    print(f"[网络] 客户端连接: {client_addr}")

    try:
        # 设置超时
        client_socket.settimeout(5.0)

        # 接收请求数据
        raw_request = client_socket.recv(1024).decode("utf-8")
        if not raw_request:
            print(f"[网络] 客户端 {client_addr} 发送空请求")
            client_socket.close()
            return

        print(f"[网络] 收到请求: {raw_request[:100]}...")  # 打印前100个字符

        # 解析请求
        method, path, headers, body = request_parser.parse_raw_request(
            client_socket, raw_request
        )
        if method is None:
            print(f"[解析] 无效请求来自 {client_addr}")
            response = create_http_response("无效请求", 400)
            client_socket.send(response.encode("utf-8"))
            client_socket.close()
            return

        # 提取命令
        command = request_parser.extract_command(method, path, body)
        print(f"[解析] 提取到命令: {command}")

        # 执行命令
        response_text, status_code = controller.execute_command(wlan, command)
        print(f"[执行] 响应: {response_text}")

        # 发送响应
        response = create_http_response(response_text, status_code)
        client_socket.send(response.encode("utf-8"))
    except OSError as e:
        # 超时错误号 110
        if e.args[0] == errno.ETIMEDOUT:
            print(f"[网络] 客户端 {client_addr} 请求超时")
        else:
            print(f"[网络] 套接字错误: {e}")
    except Exception as e:
        print(f"[错误] 处理客户端 {client_addr} 时: {e}")
    finally:
        # 确保关闭连接
        try:
            client_socket.close()
        except:
            pass
        print(f"[网络] 客户端 {client_addr} 连接关闭")


def create_http_response(body: str, status_code: int = 200) -> str:
    """纯网络功能：创建HTTP响应"""
    status_text = "OK" if status_code == 200 else "Bad Request"
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n\r\n"
        f"{body}"
    )
    return response
