from scapy.all import IP

from abc import ABC, abstractmethod
from typing import Optional

class Probe(ABC):
    @abstractmethod
    def send(self, dst_ip: str, ttl: int, **kwargs) -> Optional[IP]:
        pass

    @abstractmethod
    def receive(self, timeout: float = 2) -> Optional[IP]:
        pass
