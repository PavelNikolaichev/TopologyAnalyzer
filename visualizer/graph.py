import networkx as nx
from traceroute.results import TraceResult

def build_topology(results: list[TraceResult]) -> nx.Graph:
    G = nx.DiGraph()

    for trace in results:
        prev = None
        for hop in trace.hops:
            G.add_node(hop.ip, hostname=hop.hostname)

            if prev:
                G.add_edge(prev, hop.ip, protocol=hop.protocol, rtt=hop.rtt, loss=hop.loss)
            
            prev = hop.ip
    
    return G
