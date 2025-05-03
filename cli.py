import sys
from traceroute import parser
from traceroute.runner import run_traceroute
import os


def main():
    arg_parser = parser.get_arg_parser()
    args = arg_parser.parse_args()

    # Read IP addresses from input file
    with open(args.input) as f:
        ips = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    if not ips:
        print("No IP addresses found in input file.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(ips)} IP addresses.")

    output_file = os.path.splitext(args.input)[0] + "_trace_results.txt"
    if hasattr(args, 'output') and args.output:
        output_file = args.output

    all_results = []
    for ip in ips:
        print(f"Tracing {ip}...")
        result = run_traceroute(
            ip,
            max_ttl=args.m,
            init_ttl=args.M,
            series=args.series,
            dport=args.p or 33434,
            wait=args.wait,
            resolve_host=not args.n
        )
        all_results.append(result)

    # Write raw results to text file
    with open(output_file, "w") as f:
        for trace in all_results:
            f.write(f"Trace to {trace.destination}:\n")
            for hop in trace.hops:
                f.write(f"TTL {hop.ttl}: {hop.ip} ({hop.hostname or ''}) [{hop.protocol}] RTT={hop.rtt:.2f}ms {'LOSS' if hop.loss else ''}\n")
            f.write("\n")

    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
