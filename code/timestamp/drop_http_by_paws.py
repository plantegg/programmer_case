from scapy.all import *

# 目标 IP 和端口
target_ip = "gf"
target_port = 8000

# 构建 HTTP GET 请求
http_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {target_ip}:{target_port}\r\n"
    "User-Agent: Mozilla/5.0\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n"
    "\r\n"
)
seq_num=1234567

# 创建 IP 层
ip = IP(dst=target_ip)

# 创建 TCP 层，设置 SYN
tcp = TCP(sport=RandShort(), dport=target_port, flags="S", seq=seq_num, options=[('MSS', 1460), ('NOP', None), ('NOP', None), ('Timestamp', (int(time.time()), 0))])

# 发送 SYN 包并接收响应
syn_ack = sr1(ip/tcp, timeout=10)

if syn_ack is None:
    print("No response received")
    exit()

# 发送 ACK
tcp_ack = TCP(sport=syn_ack[TCP].dport, 
              dport=target_port,
              flags="A", 
              seq=syn_ack[TCP].ack,
              ack=syn_ack[TCP].seq + 1)

# 发送 HTTP GET 请求
tcp_push = TCP(sport=syn_ack[TCP].dport,
               dport=target_port,
               flags="PA",
               seq=syn_ack[TCP].ack,
               ack=syn_ack[TCP].seq + 1,
               options=[('MSS', 1460), ('NOP', None), ('NOP', None), ('Timestamp', (0, 0))])

# 发送请求并接收响应
response = sr1(ip/tcp_push/http_request, timeout=10)

if response:
    # 打印响应内容
    if Raw in response:
        print(response[Raw].load.decode())
else:
    print("No response received")

# 发送 FIN 包关闭连接
fin = ip/TCP(sport=syn_ack[TCP].dport,
             dport=target_port,
             flags="FA",
             seq=syn_ack[TCP].ack,
             ack=syn_ack[TCP].seq + 1)
send(fin)

