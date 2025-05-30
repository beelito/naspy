import hashlib

class Datom:
    def __init__(self, dtype: str, value):
        self.dtype = dtype
        self.value = value
        self.hash = self.compute_hash()

    def compute_hash(self):
        encoded = f"{self.dtype}:{repr(self.value)}".encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def __repr__(self):
        return f"Datom({self.dtype}, {repr(self.value)})"