import hashlib

class DataculeStream:
    def __init__(self):
        self.stream: list[tuple[str, list[str]]] = []

    def add_datacule(self, datacule: list[str]) -> None:
        datacule_hash = self._compute_hash(datacule)
        self.stream.append((datacule_hash, datacule))

    def _compute_hash(self, hash_list: list[str]) -> str:
        combined = "".join(hash_list).encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def query(self, predicate):
        return [
            (h, hashes) for h, hashes in self.stream
            if predicate(hashes)
        ]

    def __len__(self):
        return len(self.stream)

    def __iter__(self):
        return iter(self.stream)