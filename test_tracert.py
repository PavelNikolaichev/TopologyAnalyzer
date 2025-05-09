import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime


def run_windows_tracert(target, max_hops=30, timeout_ms=4000, resolve_names=True):
    """
    Run tracert command on a target and return the output. Used for a sanity check, should work on any os.
    
    Args:
        target (str): Target hostname or IP address
        max_hops (int): Maximum number of hops (TTL)
        timeout_ms (int): Timeout in milliseconds
        resolve_names (bool): Whether to resolve hostnames or not
    
    Returns:
        str: Output of the tracert command
    """
    cmd = ["tracert"]
    
    if not resolve_names:
        cmd.append("-d")
    
    cmd.extend(["-h", str(max_hops)])
    cmd.extend(["-w", str(timeout_ms)])
    cmd.append(target)
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=False
        )
        return result.stdout
    except Exception as e:
        print(f"Error running tracert for {target}: {str(e)}", file=sys.stderr)
        return f"ERROR: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Windows Tracert Tool for TopologyAnalyzer")
    
    parser.add_argument("-i", "--input", required=True, help="Input CSV file with URLs (Cisco format)")
    parser.add_argument("-o", "--output", help="Output file for results (default: input_tracert_results.txt)")
    parser.add_argument("-m", "--max-hops", type=int, default=30, help="Maximum number of hops")
    parser.add_argument("-w", "--timeout", type=int, default=4000, help="Wait timeout in milliseconds")
    parser.add_argument("-n", "--no-resolve", action="store_true", help="Do not resolve hostnames")
    parser.add_argument("-l", "--limit", type=int, help="Limit number of URLs to process")
    
    args = parser.parse_args()
    
    output_file = args.output
    if not output_file:
        output_file = os.path.splitext(args.input)[0] + "_tracert_results.txt"
    
    urls = []
    try:
        with open(args.input, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    urls.append(row[1])
    except Exception as e:
        print(f"Error reading input file: {str(e)}", file=sys.stderr)
        return
    
    if args.limit and args.limit > 0:
        urls = urls[:args.limit]
    
    print(f"Loaded {len(urls)} URLs from {args.input}")
    
    with open(output_file, 'w') as f:
        f.write(f"# Windows Tracert Results\n")
        f.write(f"# Generated: {datetime.now()}\n")
        f.write(f"# Input: {args.input}\n")
        f.write(f"# Max Hops: {args.max_hops}\n")
        f.write(f"# Timeout: {args.timeout}ms\n")
        f.write(f"# Resolve Names: {not args.no_resolve}\n\n")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Tracing route to {url}...")
            
            result = run_windows_tracert(
                url,
                max_hops=args.max_hops,
                timeout_ms=args.timeout,
                resolve_names=not args.no_resolve
            )
            
            f.write(f"{'='*80}\n")
            f.write(f"URL #{i}: {url}\n")
            f.write(f"{'='*80}\n\n")
            f.write(result)
            f.write("\n\n")
    
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    main()
