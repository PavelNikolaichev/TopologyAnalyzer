import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from traceroute.results import HopResult, TraceResult

@pytest.fixture
def hop():
    return HopResult(ttl=1, ip="1.1.1.1", rtt=10.5, hostname="a.com", protocol="ICMP", loss=False)

@pytest.fixture
def trace():
    return TraceResult(destination="8.8.8.8")

def test_hop_result_fields(hop):
    assert hop.ttl == 1
    assert hop.ip == "1.1.1.1"
    assert hop.rtt == 10.5
    assert hop.hostname == "a.com"
    assert hop.protocol == "ICMP"
    assert hop.loss is False

def test_trace_result_fields(trace):
    assert trace.destination == "8.8.8.8"
    assert trace.hops == []
    assert trace.raw == ""
