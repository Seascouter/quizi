class Set:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def get_name(self):
        return self.name

class Card:
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def get_q(self):
        return self.side1

    def get_a(self):
        return self.side2
