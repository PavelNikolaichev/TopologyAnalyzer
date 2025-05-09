import re
import networkx as nx
import plotly.graph_objects as go
from collections import defaultdict
import itertools
import plotly.express as px
import math

INPUT_FILE = "ips_trace_results.txt"

PROTOCOL_COLOR = {"ICMP": "blue", "UDP": "green", "TCP": "red"}


def parse_trace(filename):
    traces = {}
    current_dest = None

    with open(filename, "r") as f:
        for raw in f:
            line = raw.strip()
            # detect new trace section
            dest_match = re.match(r"Trace to (.*):", line)
            if dest_match:
                current_dest = dest_match.group(1)
                traces[current_dest] = defaultdict(list)
                continue

            match = re.match(
                r"TTL (\d+): ([\d.]+) \((.*?)\) \[(ICMP|UDP|TCP)\] RTT=([\d.]+)ms",
                line,
            )
            if match and current_dest:
                ttl, ip, name, proto, rtt = match.groups()
                ttl = int(ttl)
                rtt = float(rtt)
                traces[current_dest][ttl].append((ip, name, proto, rtt))

    return traces


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
        data["color"] = (
            PROTOCOL_COLOR[list(data["protocols"])[0]]
            if len(data["protocols"]) == 1
            else "gray"
        )
        data["label"] = (
            f"RTT: {avg_rtt:.2f}ms\nProtocols: {', '.join(data['protocols'])}"
        )


def draw_graph(G, title="Traceroute Topology Visualization"):
    pos = nx.spring_layout(G, seed=42, k=0.5)

    # Group edges by protocol(s)
    edge_groups = defaultdict(lambda: {"x": [], "y": [], "text": [], "color": ""})

    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        label = data["label"]
        color = data["color"]
        protocol_key = (
            ", ".join(sorted(data["protocols"]))
            if len(data["protocols"]) > 1
            else list(data["protocols"])[0]
        )

        edge_groups[protocol_key]["x"] += [x0, x1, None]
        edge_groups[protocol_key]["y"] += [y0, y1, None]
        edge_groups[protocol_key]["text"].append(label)
        edge_groups[protocol_key][
            "color"
        ] = color  # same color for all edges in this group

    edge_traces = []
    for proto, group in edge_groups.items():
        edge_traces.append(
            go.Scatter(
                x=group["x"],
                y=group["y"],
                line=dict(width=2, color=group["color"]),
                hoverinfo="text",
                text=group["text"],
                mode="lines",
                name=proto,
                showlegend=True,
            )
        )

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers+text",
        hoverinfo="text",
        marker=dict(size=15, color="lightblue", line=dict(width=2)),
        textposition="bottom center",
        name="Nodes",
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["text"] += (G.nodes[node]["label"],)

    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title=title,
            showlegend=True,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        ),
    )
    fig.show()

def draw_all(traces):
    # assign a distinct color to each trace/destination
    dests = list(traces.keys())
    palette = px.colors.qualitative.Plotly
    color_map = {d: palette[i % len(palette)] for i, d in enumerate(dests)}

    # build a union graph just to compute a shared layout
    G_union = nx.DiGraph()
    for hops in traces.values():
        G = build_graph(hops)
        G_union.add_nodes_from(G.nodes(data=True))
        G_union.add_edges_from(G.edges(data=True))

    pos = nx.spring_layout(G_union, seed=42, k=0.5)

    # build one Scatter per destination
    edge_traces = []
    for dest, hops in traces.items():
        G = build_graph(hops)
        xs, ys = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            xs += [x0, x1, None]
            ys += [y0, y1, None]
        edge_traces.append(
            go.Scatter(
                x=xs, y=ys,
                mode="lines",
                line=dict(width=2, color=color_map[dest]),
                name=dest,
                hoverinfo="none",
            )
        )

    # draw nodes once
    node_trace = go.Scatter(
        x=[], y=[], text=[],
        mode="markers+text",
        hoverinfo="text",
        marker=dict(size=15, color="lightblue", line=dict(width=2)),
        textposition="bottom center",
        name="Nodes",
    )
    for n, attrs in G_union.nodes(data=True):
        x, y = pos[n]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["text"] += (attrs["label"],)

    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title="All Traces Overlaid by Destination",
            showlegend=True,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        ),
    )
    fig.show()


def main():
    traces = parse_trace(INPUT_FILE)
    draw_all(traces)

if __name__ == "__main__":
    main()
