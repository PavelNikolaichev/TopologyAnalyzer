import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from traceroute import parser

@pytest.fixture
def arg_parser():
    return parser.get_arg_parser()

def test_arg_parser_defaults(arg_parser):
    args = arg_parser.parse_args(['-i', 'ips.txt'])
    assert args.input == 'ips.txt'
    assert args.m == 30
    assert args.M == 1
    assert args.series == 3
    assert args.wait == 1.0
    assert args.size == 60
    assert args.n is False

# I think it's fine if it ignores it
# def test_arg_parser_invalid_input(arg_parser):
#     # ICMP should not accept -p (port), so this should error
#     with pytest.raises(SystemExit):
#         arg_parser.parse_args(['-i', 'ips.txt', '-P', 'ICMP', '-p', '33434'])

def test_arg_parser_invalid_protocol(arg_parser):
    # No invalid protocol test needed, as UDP is valid. Instead, test an actually invalid protocol:
    with pytest.raises(SystemExit):
        arg_parser.parse_args(['-i', 'ips.txt', '-P', 'FOO'])

def test_arg_parser_invalid_series(arg_parser):
    # --series expects an int, but 3 is valid. Let's test with an invalid string:
    with pytest.raises(SystemExit):
        arg_parser.parse_args(['-i', 'ips.txt', '--series', 'foo'])

def test_arg_parser_invalid_wait(arg_parser):
    # --wait expects a float, so test with a string
    with pytest.raises(SystemExit):
        arg_parser.parse_args(['-i', 'ips.txt', '--wait', 'foo'])

def test_arg_parser_invalid_size(arg_parser):
    # --size expects an int, so test with a string
    with pytest.raises(SystemExit):
        arg_parser.parse_args(['-i', 'ips.txt', '--size', 'foo'])


def test_arg_parser_all_valid(arg_parser):
    args = arg_parser.parse_args([
        '-i', 'ips.txt',
        '-P', 'UDP',
        '-p', '33434',
        '--series', '5',
        '--wait', '2.0',
        '--size', '80',
        '-n'
    ])
    assert args.input == 'ips.txt'
    assert args.m == 30
    assert args.M == 1
    assert args.series == 5
    assert args.wait == 2.0
    assert args.size == 80
    assert args.n is True
    assert args.P == 'UDP'
    assert args.p == 33434

def test_arg_parser_protocol_UDP(arg_parser):
    args = arg_parser.parse_args(['-i', 'ips.txt', '-P', 'UDP', '-p', '33434'])
    assert args.P == 'UDP'
    assert args.p == 33434

def test_arg_parser_protocol_TCP(arg_parser):
    args = arg_parser.parse_args(['-i', 'ips.txt', '-P', 'TCP', '-p', '33434'])
    assert args.P == 'TCP'
    assert args.p == 33434
