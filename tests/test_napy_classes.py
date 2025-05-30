import unittest
import tempfile
import os
import json

from naspy.datom import Datom
from naspy.datom_index import DatomIndex
from naspy.dataculestream import DataculeStream
from naspy.scanner import Scanner
from naspy.io import export_nason, load_nason

class TestDatom(unittest.TestCase):
    def test_datom_hash_consistency(self):
        d1 = Datom("text", "hello")
        d2 = Datom("text", "hello")
        self.assertEqual(d1.hash, d2.hash)

    def test_datom_repr(self):
        d = Datom("int", 42)
        self.assertIn("Datom(int", repr(d))


class TestDatomIndex(unittest.TestCase):
    def setUp(self):
        self.index = DatomIndex()

    def test_create_and_get(self):
        d = self.index.create("text", "name")
        self.assertEqual(self.index.get("text", "name"), d)

    def test_deduplication(self):
        d1 = self.index.create("symbol", "+")
        d2 = self.index.create("symbol", "+")
        self.assertIs(d1, d2)
        self.assertEqual(len(self.index), 1)


class TestScanner(unittest.TestCase):
    def setUp(self):
        self.index = DatomIndex()
        self.scanner = Scanner(self.index)

    def test_observe_dict(self):
        obj = {"name": "user", "age": 25}
        datacule = self.scanner.observe(obj)
        self.assertEqual(len(datacule), 2)

    def test_observe_object(self):
        class Dummy:
            def __init__(self):
                self.x = 1
                self.y = 2

        d = Dummy()
        datacule = self.scanner.observe(d)
        self.assertEqual(len(datacule), 2)

    def test_nested_dict(self):
        obj = {"user": {"id": "u1", "name": "Bee"}}
        datacule = self.scanner.observe(obj)
        self.assertTrue(any("user.id" in k or "user.name" in k for k, _ in self.index.index))


class TestDataculeStream(unittest.TestCase):
    def setUp(self):
        self.stream = DataculeStream()

    def test_add_and_len(self):
        datacule = ["abc123", "def456"]
        self.stream.add_datacule(datacule)
        self.assertEqual(len(self.stream), 1)

    def test_hash_is_correct(self):
        datacule = ["1", "2", "3"]
        self.stream.add_datacule(datacule)
        expected_hash = self.stream._compute_hash(datacule)
        self.assertEqual(self.stream.stream[0][0], expected_hash)

    def test_iterate(self):
        hashes = ["a", "b"]
        self.stream.add_datacule(hashes)
        for item in self.stream:
            self.assertIsInstance(item, tuple)


class TestIO(unittest.TestCase):
    def setUp(self):
        self.index = DatomIndex()
        self.stream = DataculeStream()
        self.scanner = Scanner(self.index)

        obj = {"event": "click", "user": "beelito"}
        datacule = self.scanner.observe(obj)
        self.stream.add_datacule(datacule)

        self.tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".nason")
        self.tempfile.close()

    def tearDown(self):
        os.unlink(self.tempfile.name)

    def test_export_and_load(self):
        export_nason(self.index, self.stream, self.tempfile.name)
        loaded_index, loaded_stream = load_nason(self.tempfile.name)

        self.assertEqual(len(loaded_index), len(self.index))
        self.assertEqual(len(loaded_stream), len(self.stream))

    def test_invalid_json(self):
        with open(self.tempfile.name, "w") as f:
            f.write("this is not json")

        with self.assertRaises(json.JSONDecodeError):
            load_nason(self.tempfile.name)

    def test_missing_hash_field(self):
        with open(self.tempfile.name, "w") as f:
            json.dump({"index": [{"dtype": "x", "value": 5}], "stream": []}, f)

        with self.assertRaises(AssertionError):
            load_nason(self.tempfile.name)

    def test_empty_index_and_stream(self):
        empty_index = DatomIndex()
        empty_stream = DataculeStream()
        export_nason(empty_index, empty_stream, self.tempfile.name)
        loaded_index, loaded_stream = load_nason(self.tempfile.name)
        self.assertEqual(len(loaded_index), 0)
        self.assertEqual(len(loaded_stream), 0)

    def test_large_scale(self):
        for i in range(500):
            obj = {"i": i, "val": f"v{i}"}
            datacule = self.scanner.observe(obj)
            self.stream.add_datacule(datacule)

        export_nason(self.index, self.stream, self.tempfile.name)
        loaded_index, loaded_stream = load_nason(self.tempfile.name)

        self.assertEqual(len(loaded_index), len(self.index))
        self.assertEqual(len(loaded_stream), len(self.stream))


if __name__ == '__main__':
    unittest.main()
