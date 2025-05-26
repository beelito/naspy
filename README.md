# NASPy Core

NAS (Neural Associative Structure) is a lightweight memory protocol inspired by how the human brain recalls experience. It allows any object to be broken into atomic data units (datoms), sequenced into memory paths (datacules), and permanently recorded into a verifiable ledger (The Stack).

NASPy Core is the foundational layer — no wallets, no coins, just clean memory logic.

---

## Features

- Datoms: Smallest unit of memory (e.g., characters, digits, symbols)
- Scanner: Recursively breaks down any Python object into datoms
- Datacule: Unique, timestamped identity for a structured memory path
- Ledger: Append-only log that verifies and stores datacules

---

## Installation

1. Clone the repository:

    git clone https://github.com/yourname/naspy-core.git
    cd naspy-core

2. Use the modules in your own Python project, or test them interactively:

    from scanner import Scanner
    from datacule import Datacule
    from ledger import Ledger

    scanner = Scanner()
    ledger = Ledger()

    data = {"from": "alice", "to": "bob", "amount": 100}
    path = scanner.scan(data)
    datacule = Datacule(path)

    ledger.add(datacule)
    ledger.save("stack.dat")

---

## Philosophy

Inspired by the way the brain links experiences through shared neurons, NAS creates digital memory structures that are compositional, reusable, and verifiable. It's not about storing data — it's about remembering how data is structured.

---

## License

MIT License

---

## Credits

Created by Eduardo / @beelito  
For questions or collabs, reach out or open an issue.
