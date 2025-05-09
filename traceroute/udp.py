from typing import Optional
from scapy.all import IP, UDP, sr1
from .base import Probe

class UDPProbe(Probe):
    def send(self, dst_ip: str, ttl: int, dport: int = 33434, **kwargs) -> IP:
        pkt = IP(dst=dst_ip, ttl=ttl)/UDP(dport=dport)
        return pkt

    def receive(self, pkt: IP, timeout: float = 2) -> Optional[IP]:
        resp = sr1(pkt, timeout=timeout, verbose=0)
        return resp
