# io.py
import json
from naspy.datom import Datom
from naspy.datom_index import DatomIndex
from naspy.dataculestream import DataculeStream

def export_nason(index: DatomIndex, stream: DataculeStream, filepath: str) -> None:
    data = {
        "index": [
            {
                "dtype": d.dtype,
                "value": d.value,
                "hash": d.hash
            } for d in index.index.values()
        ],
        "stream": [
            {
                "hash": datacule_hash,
                "datacule": datacule
            } for datacule_hash, datacule in stream
        ]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_nason(filepath: str) -> tuple[DatomIndex, DataculeStream]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    index = DatomIndex()
    for entry in data["index"]:
        if "hash" not in entry:
            raise ValueError("Missing 'hash' field in datom index entry")
        d = Datom(entry["dtype"], entry["value"])
        assert d.hash == entry["hash"], f"Hash mismatch: {d.hash} != {entry['hash']}"
        index.index[(d.dtype, repr(d.value))] = d

    stream = DataculeStream()
    stream.stream = [
        (entry["hash"], entry["datacule"])
        for entry in data["stream"]
    ]

    return index, stream
