from typing import Optional
from scapy.all import IP, TCP, sr1
from .base import Probe
from typing import Optional

class TCPProbe(Probe):
    def send(self, dst_ip: str, ttl: int, dport: int = 80, **kwargs) -> IP:
        pkt = IP(dst=dst_ip, ttl=ttl)/TCP(dport=dport, flags='S')
        return pkt

    def receive(self, pkt: IP, timeout: float = 2) -> Optional[IP]:
        resp = sr1(pkt, timeout=timeout, verbose=0)
        return resp
