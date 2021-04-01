class Node:
    def __init__(self, n_id, ports):
        self.id = n_id
        self.ports = ports

    def allPortTaken(self):
        return all([p.taken for p in self.ports])

    def deg(self):
        return len(self.ports)

    def to_string(self):
        print("id:", self.id, "ports:", self.ports)


class Port:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.taken = False

    def to_string(self):
        print("n1:", self.n1, "n2:", self.n2, "taken: ", self.taken)

    def equals(self, other):
        return other is not None and self.n1 == other.n1 and self.n2 == other.n2
