from collections import Counter

import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms.components import connected_components


def count_nodes_per_level(G):
    results = []
    for component in connected_components(G):
        levels = {}
        visited = set()
        if not component:
            results.append(levels)
            continue
        root = next(iter(component))
        current_level = [root]
        while current_level:
            next_level = []
            for node in current_level:
                if node not in visited:
                    visited.add(node)
                    level = nx.shortest_path_length(G, source=root, target=node)
                    if level not in levels:
                        levels[level] = 0
                    levels[level] += 1
                    next_level.extend(G.neighbors(node))
            current_level = next_level
        results.append(levels)
    return results


def average_dicts(dicts):
    avg_dict = {}
    count_dict = {}
    for d in dicts:
        for key, value in d.items():
            if key not in avg_dict:
                avg_dict[key] = 0
                count_dict[key] = 0
            avg_dict[key] += value
            count_dict[key] += 1
    for key in avg_dict:
        avg_dict[key] /= count_dict[key]
        avg_dict[key] = round(avg_dict[key], 3)
    return avg_dict


def number_children(G):
    avgs = average_dicts(count_nodes_per_level(G))

    fig = plt.figure(figsize=(12, 8))
    plt.bar(avgs.keys(), avgs.values())
    # plt.title('')
    plt.xlabel('Level')
    plt.ylabel('Num Children')
    for key, value in avgs.items():
        plt.text(key, value + 0.1, f'{value:.3f}', ha='center')
    plt.show()


def number_of_graphs(G):
    key_counts = Counter(key for d in count_nodes_per_level(G) for key in d)
    fig = plt.figure(figsize=(12, 8))
    plt.bar(key_counts.keys(), key_counts.values())
    # plt.title('')
    plt.xlabel('Num Children')
    plt.ylabel('Number of graphs')
    for key, value in key_counts.items():
        plt.text(key, value + 0.1, f'{value:d}', ha='center')
    plt.show()


def count_children(G):
    children_count = {}
    i = 0
    for node in G.nodes():
        children_count[f"Level {i}"] = len(list(G.neighbors(node)))
        i += 1
    return children_count


def count_children(G):
    children_counts = []
    for component in nx.connected_components(G):
        component_counts = {}
        i = 0
        for node in component:
            component_counts[f"Level {i}"] = len(list(G.neighbors(node)))
            i += 1
        children_counts.append(component_counts)
    if len(children_counts) == 1:
        return children_counts[0]
    else:
        return children_counts

def error_count(alldf):
    fig = plt.figure(figsize=(12, 10))

    # Plot the bar chart
    ax = alldf['IsError'].value_counts().plot(kind='bar', color=['red', 'green'])

    # Add labels above each bar with the corresponding value
    for i, v in enumerate(alldf['IsError'].value_counts()):
        ax.text(i, v + 0.1, f'{v}', ha='center')

    # Set the x-axis and y-axis labels
    ax.set_xlabel('IsError', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    # Set the title of the plot
    ax.set_title('Error Counts', fontsize=16)

    # Show the plot
    plt.show()

def span_type_count(alldf):
    fig = plt.figure(figsize=(12, 10))

    # Plot the bar chart
    ax = alldf['SpanType'].value_counts().plot(kind='bar', color=['red', 'green', 'yellow'])

    # Add labels above each bar with the corresponding value
    for i, v in enumerate(alldf['SpanType'].value_counts()):
        ax.text(i, v + 0.1, f'{v}', ha='center')

    # Set the x-axis and y-axis labels
    ax.set_xlabel('SpanType', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    # Set the title of the plot
    ax.set_title('SpanType Counts', fontsize=16)

    # Show the plot
    plt.show()

def peer_types_count(alldf):
    # Create a new figure with the specified size
    fig = plt.figure(figsize=(12, 10))

    # Plot the bar chart
    ax = alldf['Peer'].value_counts().plot(kind='bar')

    # Set the x-axis and y-axis labels
    ax.set_xlabel('Peer', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    # Set the title of the plot
    ax.set_title('Peer types', fontsize=16)

    # Show the plot
    plt.show()


def component_types(alldf):
    fig = plt.figure(figsize=(12, 10))

    # Plot the bar chart
    ax = alldf['Component'].value_counts().plot(kind='bar')

    # Add labels above each bar with the corresponding value
    for i, v in enumerate(alldf['Component'].value_counts()):
        ax.text(i, v + 0.1, f'{v}', ha='center')

    # Set the x-axis and y-axis labels
    ax.set_xlabel('Component', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    # Set the title of the plot
    ax.set_title('Component types', fontsize=16)

    # Show the plot
    plt.show()