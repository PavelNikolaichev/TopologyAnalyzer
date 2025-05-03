import argparse

def get_arg_parser():
    parser = argparse.ArgumentParser(description="Internet Topology Explorer")
    
    parser.add_argument("-i", "--input", required=True, help="Input file with IP addresses")
    parser.add_argument("-n", action="store_true", help="Do not resolve hostnames")
    parser.add_argument("-m", type=int, default=30, help="Max TTL")
    parser.add_argument("-M", type=int, default=1, help="Initial TTL")
    parser.add_argument("-P", choices=["ICMP", "UDP", "TCP"], help="Protocol")
    parser.add_argument("-p", type=int, help="Destination port (UDP/TCP)")
    parser.add_argument("--series", type=int, default=3, help="Number of probe series per hop")
    parser.add_argument("--wait", type=float, default=1.0, help="Wait time between probes (s)")
    parser.add_argument("--size", type=int, default=60, help="Packet size in bytes")

    return parser
