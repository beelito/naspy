from naspy.datom_index import DatomIndex

class Scanner:
    def __init__(self, index: DatomIndex):
        self.index = index

    def observe(self, raw_input) -> list[str]:
        flat = self._flatten(raw_input)

        datom_hashes = []
        for dtype, value in flat:
            datom = self.index.create(dtype, value)
            datom_hashes.append(datom.hash)

        return datom_hashes

    def _flatten(self, data, prefix=""):
        out = []

        if isinstance(data, dict):
            for k, v in data.items():
                key = f"{prefix}.{k}" if prefix else k
                out.extend(self._flatten(v, key))

        elif hasattr(data, "__dict__"):
            return self._flatten(vars(data), prefix)

        elif isinstance(data, (list, tuple)) and not isinstance(data, str):
            for i, v in enumerate(data):
                key = f"{prefix}[{i}]" if prefix else str(i)
                out.extend(self._flatten(v, key))

        else:
            out.append((prefix, data))

        return out