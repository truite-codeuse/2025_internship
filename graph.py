import networkx as nx
import matplotlib.pyplot as plt
import re
import sys


class Graph():

    def __init__(self, nodes, attacks):
        self._nodes = nodes
        self._attacks = attacks

    def node_exists(self, node):
        return node in self._nodes

    def attack_exists(self, attack) -> bool:
        return attack in self._attacks

    def get_nodes(self):
        return self._nodes

    def get_attacks(self):
        return self._attacks

    def get_direct_attackers(self, node) -> list:
        if node not in self._nodes:
            return []
        res = []
        for att in self._attacks:
            if node == att[1] and att[0] not in res:
                res.append(att[0])
        return res

    def print_graph(self):
        graph_viz = nx.DiGraph()
        graph_viz.add_edges_from(self._attacks)
        nx.draw_networkx(graph_viz, pos=nx.spring_layout(graph_viz, k=0.3, iterations=50))
        plt.show()


def read_graph_from_file(filename):
    nodes = []
    attacks = []
    with open(filename, 'r') as f:
        for line in f:
            line_str = line.strip().replace('\n', '')
            if ',' not in line_str:
                node = re.search(r'\(([^)]+)', line_str).group(1)
                if node not in nodes:
                    nodes.append(node)
            else:
                attack = re.search(r'\(([^)]+)', line_str).group(1).split(',')
                if attack[0] in nodes and attack[1] in nodes and attack not in attacks:
                    attacks.append(attack)
    return Graph(nodes, attacks)


if __name__ == "__main__":
    filename = sys.argv[1]
    if ".apx" in filename:
        g = read_graph_from_file(filename)
        g.print_graph()
