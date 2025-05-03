import time
from .icmp import ICMPProbe
from .udp import UDPProbe
from .tcp import TCPProbe
from .results import HopResult, TraceResult

def run_traceroute(dst_ip: str, max_ttl: int = 30, init_ttl: int = 1, series: int = 3, dport: int = 33434, wait: float = 1.0, resolve_host: bool = False) -> TraceResult:
    probes = [ICMPProbe(), UDPProbe(), TCPProbe()]
    protocols = ['ICMP', 'UDP', 'TCP']
    
    trace = TraceResult(destination=dst_ip)
    
    for ttl in range(init_ttl, max_ttl + 1):
        for _ in range(series):
            for probe, proto in zip(probes, protocols):
                pkt = probe.send(dst_ip, ttl, dport=dport)
                
                start = time.time()
                resp = probe.receive(pkt)
                rtt = (time.time() - start) * 1000  # ms
                
                if resp is None:
                    hop = HopResult(ttl=ttl, ip='*', rtt=0, protocol=proto, loss=True)
                else:
                    ip = resp.src
                    hostname = None
                    
                    if resolve_host and ip != '*':
                        try:
                            import socket
                            hostname = socket.gethostbyaddr(ip)[0]
                        except Exception:
                            hostname = None
                    
                    hop = HopResult(ttl=ttl, ip=ip, rtt=rtt, protocol=proto, hostname=hostname, loss=False)
                
                trace.hops.append(hop)
                
                time.sleep(wait)

        # Stop if destination is reached
        if any(hop.ip == dst_ip for hop in trace.hops[-3*series:]):
            break

    return trace
