from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class HopResult:
    ttl: int
    ip: str
    rtt: float
    hostname: Optional[str] = None
    protocol: str = "ICMP"
    loss: bool = False

@dataclass
class TraceResult:
    destination: str
    hops: List[HopResult] = field(default_factory=list)
    raw: str = ""
