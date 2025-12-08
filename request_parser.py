def parse_raw_request(
    client_socket: socket.socket,  # 新增：需要继续读 body
    raw_request: str,
) -> Tuple[Optional[str], Optional[str], Dict[str, str], str]:
    """
    纯解析功能：解析原始 HTTP 请求
    返回: (method, path, headers, body)
    """
    lines = raw_request.strip().split("\r\n")
    if not lines or lines[0] == "":
        return None, None, {}, ""

    # ----- 1. 请求行 -----
    request_line = lines[0]
    parts = request_line.split(" ")
    if len(parts) < 2:
        return None, None, {}, ""

    method = parts[0]
    path = parts[1]

    # ----- 2. 头部 -----
    headers: Dict[str, str] = {}
    body_start_idx = 1
    for i, line in enumerate(lines[1:], start=1):
        if line == "":  # 空行代表头部结束
            body_start_idx = i + 1
            break
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()  # 统一小写，方便后面取值

    # ----- 3. body（可能分片） -----
    # 3-a 先看头部里有没有声明长度
    content_len = int(headers.get("content-length", 0))

    # 3-b 如果已经有部分 body 落在 raw_request 里（HTTP/1.1 很常见）
    partial_body = (
        "\r\n".join(lines[body_start_idx:]) if body_start_idx < len(lines) else ""
    )
    body = partial_body

    # 3-c 剩余长度继续 recv
    remain = content_len - len(body.encode("utf-8"))  # 按字节算
    while remain > 0:
        try:
            chunk = client_socket.recv(min(remain, 512))
            if not chunk:  # 对方关闭
                break
            body += chunk.decode("utf-8", "ignore")
            remain -= len(chunk)
        except:
            break

    print(
        f"[解析] 方法={method}, 路径={path}, Content-Length={content_len}, 实际 body 长度={len(body.encode('utf-8'))}"
    )
    return method, path, headers, body


def extract_command(method: str, path: str, body: str) -> str:
    """
    纯解析功能：从解析结果中提取具体命令
    简化版：每种功能只支持单一命令格式
    """
    # GET 请求：从路径提取命令
    if method == "GET":
        # 移除路径开头的斜杠和查询参数
        clean_path = path.split("?")[0].strip("/").upper()
        return clean_path
    # POST 请求：从正文提取命令
    elif method == "POST":
        clean_body = body.strip().upper()
        return clean_body
    return "UNKNOWN"
