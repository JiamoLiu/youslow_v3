from scapy.all import *

def handle_packet(packet):
    print(packet.summary())

# Capture 10 packets
packets = sniff(count=10)

# Print summary of each packet
for packet in packets:
    handle_packet(packet)

# Save captured packets to a file
wrpcap('captured_traffic.pcap', packets)
