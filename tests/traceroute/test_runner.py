import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from unittest.mock import patch, MagicMock
from traceroute.runner import run_traceroute

@patch('traceroute.runner.ICMPProbe')
@patch('traceroute.runner.UDPProbe')
@patch('traceroute.runner.TCPProbe')
def test_run_traceroute_mocks(MockTCP, MockUDP, MockICMP):
    # Setup separate mocks for each probe type
    icmp_probe = MagicMock()
    udp_probe = MagicMock()
    tcp_probe = MagicMock()

    icmp_probe.send.return_value = 'icmp_pkt'
    udp_probe.send.return_value = 'udp_pkt'
    tcp_probe.send.return_value = 'tcp_pkt'

    # For each probe, return '1.1.1.1' for the first TTL, then '2.2.2.2' for the second TTL
    icmp_probe.receive.side_effect = [MagicMock(src='1.1.1.1'), MagicMock(src='2.2.2.2')]
    udp_probe.receive.side_effect = [MagicMock(src='1.1.1.1'), MagicMock(src='2.2.2.2')]
    tcp_probe.receive.side_effect = [MagicMock(src='1.1.1.1'), MagicMock(src='2.2.2.2')]

    MockICMP.return_value = icmp_probe
    MockUDP.return_value = udp_probe
    MockTCP.return_value = tcp_probe

    result = run_traceroute('2.2.2.2', max_ttl=2, init_ttl=1, series=1, dport=33434, wait=0, resolve_host=False)
    
    # Should have 2 TTLs * 3 protocols = 6 hops
    assert len(result.hops) == 6
    
    # First 3 hops should have ip '1.1.1.1', last 3 should have '2.2.2.2'
    for hop in result.hops[:3]:
        assert hop.ip == '1.1.1.1'
        assert not hop.loss
        assert hop.rtt >= 0

    for hop in result.hops[3:]:
        assert hop.ip == '2.2.2.2'
        assert not hop.loss
        assert hop.rtt >= 0
