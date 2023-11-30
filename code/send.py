from scapy.all import *
import time
import sys

target_ip = "server_host_ip"
target_port = 22345
src_port=random.randint(1024,65535)
#src_port=12345
init_seq=4294967292

ip = IP(dst=target_ip)
syn = TCP(sport=src_port, dport=target_port, flags="S", seq=init_seq)
syn_ack = sr1(ip / syn)
if syn_ack and TCP in syn_ack and syn_ack[TCP].flags == "SA":
    print("Received SYN-ACK")
    ack = TCP(sport=src_port, dport=target_port,
              flags="A", seq=syn_ack.ack, ack=syn_ack.seq+1)
    print(syn_ack.seq)
    print(syn_ack.ack)
    print(ack)
    send(ip/ack)
    print("Send ACK")
else:
    print("Failed to establish TCP connection")
    
print("send payload")  
data="rrr"
payload=TCP(sport=src_port, dport=22345,flags="AP", seq=syn_ack.ack,  ack=syn_ack.seq+1)
payload2=TCP(sport=src_port, dport=22345,flags="AP", seq=0,  ack=syn_ack.seq+1)
syn_ack=send(ip/payload/Raw(load=data))
syn_ack=send(ip/payload2/Raw(load=data))
