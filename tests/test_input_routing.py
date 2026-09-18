import tempfile
import unittest
from pathlib import Path

from scripts import prepare_meeting_input as preparation


class InputRoutingTests(unittest.TestCase):
    def test_text_input_does_not_use_bailian(self):
        with tempfile.TemporaryDirectory() as temp:
            root_path = Path(temp)
            source = root_path / "meeting.md"
            source.write_text("# Notes\n\nA confirmed decision.", encoding="utf-8")
            output = root_path / "out"
            manifest = preparation.prepare([source], output, "auto", "MISSING_KEY")
            self.assertFalse(manifest["used_bailian"])
            self.assertEqual(manifest["input_kinds"], ["text"])
            self.assertIn("A confirmed decision.", Path(manifest["transcript_path"]).read_text(encoding="utf-8"))

    def test_audio_extension_is_routed_to_bailian(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "meeting.wav"
            source.write_bytes(b"not-a-real-audio-file")
            self.assertEqual(preparation.detect_kind(source), "audio")

    def test_unknown_utf8_file_is_text(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "meeting.custom"
            source.write_text("timestamped transcript", encoding="utf-8")
            self.assertEqual(preparation.detect_kind(source), "text")


if __name__ == "__main__":
    unittest.main()
