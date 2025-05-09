from scapy.all import IP, ICMP, sr1
from typing import Optional
from .base import Probe


class ICMPProbe(Probe):
    def send(self, dst_ip: str, ttl: int, **kwargs) -> IP:
        pkt = IP(dst=dst_ip, ttl=ttl) / ICMP()
        return pkt

    def receive(self, pkt: IP, timeout: float = 2) -> Optional[IP]:
        resp = sr1(pkt, timeout=timeout, verbose=0)
        return resp
