# udp_server.py
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"🔌 Listening on {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"📨 Received from {addr}: {data.decode(errors='ignore')}")

    # Send reply (can be audio/text)
    reply = "Acknowledged"
    sock.sendto(reply.encode(), addr)
