# TopologyAnalyzer

Internet topology explorer and visualizer in Python.

## Features
- Traceroute-like probing supporting ICMP, UDP, and TCP
- Configurable probe options (TTL, protocol, port, etc.)
- Batch processing of IP lists
- Interactive visualization of discovered network paths

## Usage
- Install dependencies:
```
pip install -r requirements.txt
```
- Run `python cli.py --help` for command-line options.
- Place your target IPs in a `.txt` or `.csv` file.

## Testing
Run all tests with:
```
pytest
```
