import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from analyze import analyze  # noqa: E402


class AnalyzeTests(unittest.TestCase):
    def test_short_text_rejected(self):
        with self.assertRaises(ValueError):
            analyze("Too short.")

    def test_repetitive_text_scores_higher_repetition(self):
        repetitive = "the cat sat on the mat. " * 12
        varied = (
            "Rain fell overnight, flooding the low road near the market. "
            "By morning, volunteers had gathered with boats and ropes. "
            "Nobody expected the water to rise so quickly, and several families "
            "waited on rooftops until help arrived from the next village."
        )
        self.assertGreater(
            analyze(repetitive)["repeated_phrase_ratio"],
            analyze(varied)["repeated_phrase_ratio"],
        )

    def test_bengali_text_runs(self):
        text = "\u09ac\u09a8\u09cd\u09af\u09be\u09b0 \u09aa\u09be\u09a8\u09bf \u09ac\u09be\u09a1\u09bc\u099b\u09bf\u09b2\u0964 " * 15
        result = analyze(text)
        self.assertGreaterEqual(result["words"], 30)


if __name__ == "__main__":
    unittest.main()
