"""核对原始字节、清单和记录的可读性。"""

from pathlib import Path
import tempfile
import unittest

from fixture_io import read_catalog, read_payload, read_records


class InputsTests(unittest.TestCase):
    root = Path(__file__).resolve().parents[1] / "examples"

    def test_catalog_covers_payload_directory(self):
        manifest = read_catalog(self.root)
        names = set(manifest["payloads"])
        self.assertEqual(names, {path.stem for path in (self.root / "payloads").glob("*.bin")})
        self.assertEqual(len(names), 5)
        for name in names:
            self.assertGreater(len(read_payload(self.root, manifest, name)), 0)

    def test_records_reference_available_payloads(self):
        manifest = read_catalog(self.root)
        lengths = []
        for name in ["shift", "comparison"]:
            rows = list(read_records(self.root / (name + ".jsonl")))
            lengths.append(len(rows))
            for record in rows:
                if "payload" in record:
                    self.assertIn(record["payload"], manifest["payloads"])
        self.assertEqual(lengths, [13, 6])

    def test_reader_rejects_backwards_clock(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "order.jsonl"
            source.write_text('{"time":2,"kind":"read"}\n{"time":1,"kind":"write"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "order.jsonl:2"):
                list(read_records(source))
