import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from traceroute.results import HopResult, TraceResult
from visualizer.graph import build_topology
import pytest

@pytest.fixture
def hops():
    return [HopResult(ttl=1, ip='1.1.1.1', rtt=10, protocol='ICMP'), HopResult(ttl=2, ip='2.2.2.2', rtt=20, protocol='UDP')]

def test_build_topology_basic(hops):
    result = TraceResult(destination='8.8.8.8', hops=hops)
    G = build_topology([result])

    # nodes should be all hop IPs
    assert set(G.nodes()) == {'1.1.1.1', '2.2.2.2'}
    
    # single edge between hops
    assert G.has_edge('1.1.1.1', '2.2.2.2')
    
    # edge data should match last hop
    data = G.edges['1.1.1.1', '2.2.2.2']
    assert data['protocol'] == 'UDP'
    assert data['rtt'] == 20
    assert data['loss'] is False

def test_build_topology_merge_traces():
    trace1 = TraceResult(destination='t1', hops=[
        HopResult(ttl=1, ip='1.1.1.1', rtt=5, protocol='ICMP'),
        HopResult(ttl=2, ip='2.2.2.2', rtt=10, protocol='UDP')
    ])
    trace2 = TraceResult(destination='t2', hops=[
        HopResult(ttl=1, ip='2.2.2.2', rtt=15, protocol='TCP'),
        HopResult(ttl=2, ip='3.3.3.3', rtt=25, protocol='ICMP', loss=True)
    ])
    G = build_topology([trace1, trace2])

    # nodes from both traces
    assert set(G.nodes()) == {'1.1.1.1', '2.2.2.2', '3.3.3.3'}
    
    # edge from trace1
    d12 = G.edges['1.1.1.1', '2.2.2.2']
    assert d12['protocol'] == 'UDP' and d12['rtt'] == 10 and d12['loss'] is False
    
    # edge from trace2
    d23 = G.edges['2.2.2.2', '3.3.3.3']
    assert d23['protocol'] == 'ICMP' and d23['rtt'] == 25 and d23['loss'] is True

def test_build_topology_hostname_attribute():
    hops_list = [
        HopResult(ttl=1, ip='1.1.1.1', rtt=5, hostname='h1', protocol='ICMP'),
        HopResult(ttl=2, ip='2.2.2.2', rtt=10, hostname=None, protocol='UDP')
    ]
    
    G = build_topology([TraceResult(destination='d', hops=hops_list)])
    
    assert G.nodes['1.1.1.1']['hostname'] == 'h1'
    assert 'hostname' in G.nodes['2.2.2.2'] and G.nodes['2.2.2.2']['hostname'] is None
