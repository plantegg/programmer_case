from scapy.all import *
import random

# 目标服务器信
target_ip = "gf"
target_port = 8000

# 源端口使用随机端口
source_port = random.randint(1024, 65535)
#source_port = 12345 

# 初始序列号
seq_num = 12345
#seq_num = random.randint(0, 4294967295)

def send_syn():
    # 构建 SYN 包
    ip = IP(dst=target_ip)
    tcp_options = [('Timestamp', (int(time.time()), 0))]
    
    syn = TCP(sport=source_port, dport=target_port, flags='S', seq=seq_num, options=tcp_options)
    syn_packet = ip/syn
    
    # 发送 SYN 并等待响应
    syn_ack = sr1(syn_packet)
    return syn_ack

def send_rst(syn_ack_packet):
    # 构建 RST 包，设置特定的 timestamp options
    ip = IP(dst=target_ip)
    
    # 创建 TCP timestamp option
    # timestamp 值为 0，echo reply 值使用服务器发来的 timestamp
    ts_val = 0
    ts_ecr = 0
    
    # 从 SYN+ACK 包中获取 timestamp
    for option in syn_ack_packet[TCP].options:
        if option[0] == 'Timestamp':
            ts_ecr = option[1][0]  # 使用服务器的 timestamp
            break
    
    tcp_options = [('Timestamp', (ts_val, ts_ecr))]
    #tcp_options = [('Timestamp', (int(time.time()), 0))]
    
    # 构建 RST 包
    rst = TCP(
        sport=source_port,
        dport=target_port,
        flags='R',
        #seq=1,
        #ack=syn_ack_packet[TCP].seq + 1,
        seq=syn_ack_packet[TCP].ack,
        options=tcp_options
    )
    
    rst_packet = ip/rst
    send(rst_packet)

def send_ack(syn_ack_packet):
    # 构建 ACK 包
    ip = IP(dst=target_ip)
    tcp_options = [('Timestamp', (int(time.time()), 0))]
    ack = TCP(
        sport=source_port,
        dport=target_port,
        flags='A',
        seq=syn_ack_packet[TCP].ack,
        ack=syn_ack_packet[TCP].seq + 1,
        options=tcp_options
    )
    
    ack_packet = ip/ack
    send(ack_packet)

def main():
    try:
        # 发送 SYN 并接收 SYN+ACK
        print("Sending SYN...")
        syn_ack = send_syn()
        
        if syn_ack and TCP in syn_ack and syn_ack[TCP].flags & 0x12:  # SYN+ACK flags
            print("Received SYN+ACK")
            
            # 发送 RST
            print("Sending RST with timestamp=0...")
            send_rst(syn_ack)
            
            # 发送 ACK
            print("Sending ACK...")
            send_ack(syn_ack)
            
            print("Sequence completed")
        else:
            print("Did not receive proper SYN+ACK")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()

