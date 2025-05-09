import re
import networkx as nx
import plotly.graph_objects as go # type: ignore
from collections import defaultdict
import math

INPUT_FILE = "ips_trace_results.txt"

PROTOCOL_COLOR = {
    "ICMP": "blue",
    "UDP": "green",
    "TCP": "red"
}

def parse_trace(filename):
    hops = defaultdict(list)

    with open(filename, 'r') as f:
        for line in f:
            match = re.match(
                r"TTL (\d+): ([\d.]+) \((.*?)\) \[(ICMP|UDP|TCP)\] RTT=([\d.]+)ms", line.strip()
            )
            if match:
                ttl, ip, name, proto, rtt = match.groups()
                ttl = int(ttl)
                rtt = float(rtt)
                hops[ttl].append((ip, name, proto, rtt))

    return hops

def build_graph(hops):
    G = nx.DiGraph()
    previous_ips = []

    for ttl in sorted(hops):
        current_ips = []
        for ip, name, proto, rtt in hops[ttl]:
            label = f"{ip}\n{name}" if name else ip
            G.add_node(ip, label=label)
            current_ips.append(ip)

            for prev_ip in previous_ips:
                if G.has_edge(prev_ip, ip):
                    G[prev_ip][ip]["rtts"].append(rtt)
                    G[prev_ip][ip]["protocols"].add(proto)
                else:
                    G.add_edge(prev_ip, ip, rtts=[rtt], protocols={proto})
        previous_ips = list(set(current_ips))  # avoid duplicate entries

    return G

def compute_edge_attributes(G):
    for u, v, data in G.edges(data=True):
        rtts = data["rtts"]
        avg_rtt = sum(rtts) / len(rtts)
        data["avg_rtt"] = avg_rtt
        data["thickness"] = max(1, 10 - math.log1p(avg_rtt))  # simulate throughput
        data["color"] = PROTOCOL_COLOR[list(data["protocols"])[0]] if len(data["protocols"]) == 1 else "gray"
        data["label"] = f"RTT: {avg_rtt:.2f}ms\nProtocols: {', '.join(data['protocols'])}"

def draw_graph(G):
    pos = nx.spring_layout(G, seed=42, k=0.5)

    # Group edges by protocol(s)
    edge_groups = defaultdict(lambda: {"x": [], "y": [], "text": [], "color": ""})

    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        label = data["label"]
        color = data["color"]
        protocol_key = ', '.join(sorted(data["protocols"])) if len(data["protocols"]) > 1 else list(data["protocols"])[0]

        edge_groups[protocol_key]["x"] += [x0, x1, None]
        edge_groups[protocol_key]["y"] += [y0, y1, None]
        edge_groups[protocol_key]["text"].append(label)
        edge_groups[protocol_key]["color"] = color  # same color for all edges in this group

    edge_traces = []
    for proto, group in edge_groups.items():
        edge_traces.append(go.Scatter(
            x=group["x"],
            y=group["y"],
            line=dict(width=2, color=group["color"]),
            hoverinfo='text',
            text=group["text"],
            mode='lines',
            name=proto,
            showlegend=True
        ))

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(size=15, color='lightblue', line=dict(width=2)),
        textposition="bottom center",
        name='Nodes'
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (G.nodes[node]['label'],)

    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title='Traceroute Topology Visualization',
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        )
    )
    fig.show()


def main():
    hops = parse_trace(INPUT_FILE)
    G = build_graph(hops)
    compute_edge_attributes(G)
    draw_graph(G)

if __name__ == "__main__":
    main()
