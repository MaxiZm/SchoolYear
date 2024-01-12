class NoHashUnorderedSet:
    def __init__(self, x):
        self.items = []
        for i in x:
            self.add(i)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def add(self, x):
        if x in self.items:
            return
        self.items.append(x)




