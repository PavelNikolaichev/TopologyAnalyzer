# HOWTO: TopologyAnalyzer

This document shows you how to install, run and visualize network traces with TopologyAnalyzer.

---

## 1. Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-org/TopologyAnalyzer.git
   cd TopologyAnalyzer
   ```
2. Create a Python virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # Powershell
   # or
   .\.venv\Scripts\activate.bat    # CMD
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Running Traceroute Batch (CLI)

TopologyAnalyzer provides a simple CLI (`cli.py`) for batch traceroute-like probing (ICMP, UDP, TCP).

Usage:
```bash
python cli.py \
  --input targets.csv \
  --output my_results.txt \
  --max-hops 30 \
  --timeout 4000 \
  --no-resolve \
  --limit 50
```

Options:
- `-i, --input`   : CSV or TXT file containing one hostname/IP per line (Cisco CSV format supported)
- `-o, --output`  : File to write results to (default: `<input>_results.txt`)
- `-m, --max-hops` : Max TTL/hops (default 30)
- `-w, --timeout`  : Probe timeout in ms (default 4000)
- `-n, --no-resolve`: Don’t perform DNS reverse lookups
- `-l, --limit`   : Stop after this many destinations

Results format:
```
Trace to 8.8.8.8:
TTL 1: 192.168.1.1 (router.local) [ICMP] RTT=1.23ms
TTL 2: * * *     [timeout]
...
```

---

## 3. OS `tracert` Wrapper

If you prefer built-in OS, or want to test the implementation of `tracert`, use the `test_tracert.py` script:

```bash
python test_tracert.py \
  --input targets.csv \
  --output tracert_out.txt \
  --max-hops 20 \
  --timeout 3000 \
  --no-resolve \
  --limit 10
```

This wraps `tracert.exe`, captures its output, and writes to your output file.

---

## 4. Visualization

Use the interactive Plotly/NetworkX visualizer at `visualizer/visualizer.py`.

1. Open `visualizer/visualizer.py` and set the path to your traceroute output:
   ```python
   INPUT_FILE = "my_results.txt"
   ```
2. Run:
   ```bash
   python visualizer/visualizer.py
   ```
3. A browser window will open showing your network topology graph:
   - Nodes represent hops
   - Edges colored by the trace they are related to
   - Hover for per-hop details

---

## 5. Testing

All unit and integration tests live alongside the code. To run them:

```bash
pytest
```

---

## 6. Tips & Troubleshooting

- Ensure you run with Administrator/Root privileges for raw ICMP probes.
- If DNS lookups are slow, use `--no-resolve`.
- Adjust `max-hops` or `timeout` for very distant hosts or poor networks.
- To embed this in other Python code, import:
  ```python
  from cli import run_all_traces
  from visualizer.visualizer import parse_trace, draw_all
  ```

Enjoy exploring your network topology!!!