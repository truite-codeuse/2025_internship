from graph import Graph

epsilon = 0.0000001

class CatSemantics():

    def __init__(self, graph: Graph):
        self._graph = graph
        self._curr_score = {
            x: 1.0 for x in graph.get_nodes()
        }
        self._epsilon = epsilon

    def get_score(self, node):
        if not self._graph.node_exists(node):
            return -1
        return self._curr_score[node]

    def compute_scores(self):
        point_fixe = 0
        while point_fixe != len(self._graph.get_nodes()):
            point_fixe = 0
            prev_score = {
                x: self._curr_score[x] for x in self._graph.get_nodes()
            }
            for node in self._graph.get_nodes():
                if len(self._graph.get_direct_attackers(node)) == 0:
                    self._curr_score[node] = prev_score[node]
                else:
                    att_sum = 0.0
                    for attacker in self._graph.get_direct_attackers(node):
                        att_sum += prev_score[attacker]
                    self._curr_score[node] = 1.0 / (1.0 + att_sum)
                if abs(self._curr_score[node] - prev_score[node]) < epsilon:
                    point_fixe += 1

    def is_stronger_or_eq(self, a, b):
        return self._curr_score[a] >= self._curr_score[b]

    def is_stronger(self, a, b):
        return self._curr_score[a] > self._curr_score[b]

    def order_to_str(self):
        order_cat = sorted(self._curr_score, key=self._curr_score.get, reverse=True)
        str_cat = ""
        for i in range(len(order_cat)):
            if str_cat == "":
                str_cat += order_cat[i]
            else:
                if self.is_stronger(order_cat[i - 1], order_cat[i]):
                    str_cat += f" > {order_cat[i]}"
                else:
                    str_cat += f" = {order_cat[i]}"
        return str_cat


class AlphaBbsSemantics():

    def __init__(self, graph: Graph, alpha):
        self._graph = graph
        self._alpha = alpha
        self._curr_score = {
            x: 1.0 for x in graph.get_nodes()
        }
        self._epsilon = epsilon

    def get_score(self, node):
        if not self._graph.node_exists(node):
            return -1
        return self._curr_score[node]

    def compute_scores(self):
        point_fixe = 0
        while point_fixe != len(self._graph.get_nodes()):
            point_fixe = 0
            prev_score = {x: self._curr_score[x] for x in self._graph.get_nodes()}
            for node in self._graph.get_nodes():
                if len(self._graph.get_direct_attackers(node)) == 0:
                    self._curr_score[node] = prev_score[node]
                else:
                    att_sum = sum(
                        [
                            1.0 / pow(prev_score[attacker], self._alpha)
                            for attacker in self._graph.get_direct_attackers(node)
                        ]
                    )
                    self._curr_score[node] = 1.0 + pow(att_sum, (1.0 / self._alpha))
                if abs(self._curr_score[node] - prev_score[node]) < epsilon:
                    point_fixe += 1


    def is_stronger_or_eq(self, a, b):
        return self._curr_score[a] <= self._curr_score[b]

    def is_stronger(self, a, b):
        return self._curr_score[a] < self._curr_score[b]

    def order_to_str(self):
        order_abbs = sorted(self._curr_score, key=self._curr_score.get, reverse=False)
        str_abbs = ""
        for i in range(len(order_abbs)):
            if str_abbs == "":
                str_abbs += order_abbs[i]
            else:
                if self.is_stronger(order_abbs[i - 1], order_abbs[i]):
                    str_abbs += f" > {order_abbs[i]}"
                else:
                    str_abbs += f" = {order_abbs[i]}"
        return str_abbs


# Kendall tau distance
def semantics_distance(nodes, sem_a, sem_b):
    disagreements = set()
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                if version == 1:
                    if (sem_a.is_stronger_or_eq(n1, n2) and sem_b.is_stronger(n2, n1)) or (sem_a.is_stronger_or_eq(n2, n1) and sem_b.is_stronger(n1, n2)):
                        disagreements.add(f"{n1},{n2}")
    return len(disagreements)
