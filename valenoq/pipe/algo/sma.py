from pdb import set_trace as stop


class Node(object):

    def __init__(self, type, value):
        self.id = id(self)
        self.type = type
        self.value = value
        self.params = None

    def __sub__(self, other):
        return SUB([self, other])

    def __add__(self, other):
        return ADD([self, other])

    def __mul__(self, other):
        return MUL([self, other])

    def __div__(self, other):
        return DIV([self, other])

    def __truediv__(self, other):
        return DIV([self, other])


class SUB(Node):
    def __init__(self, items):
        super().__init__("math", "SUB")
        self.left = items[0]
        self.right = items[1]


class ADD(Node):
    def __init__(self, items):
        super().__init__("math", "ADD")
        self.left = items[0]
        self.right = items[1]


class MUL(Node):
    def __init__(self, items):
        super().__init__("math", "MUL")
        self.left = items[0]
        self.right = items[1]


class DIV(Node):
    def __init__(self, items):
        super().__init__("math", "DIV")
        self.left = items[0]
        self.right = items[1]


class SMA(Node):

    def __init__(self, value, window):
        super().__init__("func", "SMA")
        self.params = [Node("str", value), Node("int", window)]


def sma(value, window):
    '''
    value: open|close|high|low
    window: integer
    '''
    ctx = SMA(value, window)
    return ctx
