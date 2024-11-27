from scapy.all import *
import time

# 目标服务器信息
target_ip = "172.26.137.130"
target_port = 8000

# 源端口（可以随机选择）
#source_port = 22345 
source_port = random.randint(1024, 2048)

# 初始序列号（可以随机生成）
seq_num = RandNum(0, 2**32-1)

def perform_handshake():
    # 构造 SYN 包
    ip = IP(dst=target_ip)
    syn = TCP(sport=source_port, 
              dport=target_port,
              flags='S',
              seq=seq_num,
              options=[('MSS', 1460), ('NOP', None), ('NOP', None), 
                      ('Timestamp', (int(time.time()), 0))])
    
    # 发送 SYN 并接收响应
    syn_ack = sr1(ip/syn)
    
    if syn_ack is None:
        print("No response received")
        return None

    
    # 构造 ACK 包
    ack = TCP(sport=source_port,
              dport=target_port,
              flags='A',
              seq=syn_ack.ack,
              ack=syn_ack.seq + 1,
              options=[('NOP', None), ('NOP', None), 
                      ('Timestamp', (int(time.time()), 0))])
    
    # 发送 ACK
    #send(ip/ack)

    # 构造不带 timestamp 的 RST 包
    rst = TCP(sport=source_port,
              dport=target_port,
              flags='R',
              seq=syn_ack.ack,
              options=[('NOP', None), ('NOP', None), 
                      ('Timestamp', (0, 0))],
              ack=syn_ack.seq + 1)
    
    send(ip/ack)
    # 发送 RST
    send(ip/rst)

if __name__ == "__main__":
    # 执行三次握手并发送 RST
    perform_handshake()

