# NASPy: Neural Associative Structure (Python Edition)

**NASPy** is a minimal, hash-based memory framework designed to mimic how associative memory works, storing and reconstructing structured data using atomic units. Built in Python, NASPy provides the tools to build memory streams, deduplicate data, and serialize complex structures into verifiable, non-redundant records.

---

## 🧠 Core Concepts

### 🔹 `Datom`
A "data atom," the smallest unit of memory. Each `Datom` has:
- A data type (e.g., `text`, `int`, `symbol`)
- A value (e.g., `"login"`, `42`)
- A hash computed from the above

### 🔹 `DatomIndex`
A lookup table that deduplicates datoms. Prevents storing the same value twice.

### 🔹 `Scanner`
Accepts objects (dicts, classes) and flattens them into lists of `Datom` hashes. Adds new `Datoms` to the index as needed.

### 🔹 `DataculeStream`
An append-only list of memory entries. Each entry is:
```
(datacule_hash, [datom_hash1, datom_hash2, ...])
```
Where `datacule_hash` is the hash of the ordered list of datom hashes.

### 🔹 `.nason` files
Serialized memory: stores the `DatomIndex` and `DataculeStream` as JSON. You can export and reload entire memory sessions using:
- `export_nason(index, stream, "file.nason")`
- `index, stream = load_nason("file.nason")`

---

## 📦 Installation
Clone the repo and import the package locally:
```bash
git clone https://github.com/yourname/naspy.git
cd naspy
```

Then in your Python files:
```python
from naspy.datom import Datom
from naspy.scanner import Scanner
```

---

## ✅ Usage Example
```python
from naspy.datom_index import DatomIndex
from naspy.dataculestream import DataculeStream
from naspy.scanner import Scanner
from naspy.io import export_nason, load_nason

index = DatomIndex()
stream = DataculeStream()
scanner = Scanner(index)

obj = {"user": "user", "event": "login"}
datacule = scanner.observe(obj)
stream.add_datacule(datacule)

export_nason(index, stream, "memory.nason")
```

---

## 🧪 Tests
Run the test suite from the root:
```bash
python -m unittest discover -s tests
```

---

## 🧩 Use Cases
- Cognitive memory simulation
- Game state snapshotting
- Transparent logging
- AI input tracking
- Behavioral analytics

---

## 🛠 Future Work
- NASPy CLI tools
- Visual datacule explorer
- Integration with `Feeds™`
- `.nason` file versioning and metadata

---

## 📄 License
MIT — free to use, build on, and enhance.
