from naspy.datom import Datom

class DatomIndex:
    def __init__(self):
        self.index = {}

    def create(self, dtype: str, value):
        key = (dtype, repr(value))
        if key not in self.index:
            self.index[key] = Datom(dtype, value)
        return self.index[key]

    def get(self, dtype: str, value):
        return self.index.get((dtype, repr(value)), None)

    def __len__(self):
        return len(self.index)