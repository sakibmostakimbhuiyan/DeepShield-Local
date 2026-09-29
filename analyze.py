"""DeepShield-Local: experimental text heuristics.

Computes simple statistical signals (sentence-length variation, vocabulary
diversity, repeated phrases) and reports which signals look unusual.
This is NOT a trained deepfake/AI-text detector. See README for limitations.
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter

SENTENCE_END = re.compile(r"[.!?\u0964]+")  # includes the Bengali danda
STRIP_CHARS = ".,;:!?\"'()[]{}<>-\u2014\u2013\u2026\u0964\u201c\u201d\u2018\u2019"

# Illustrative thresholds. They are NOT calibrated on real data.
LOW_BURSTINESS = 0.30
LOW_DIVERSITY = 0.45
HIGH_REPETITION = 0.10
MIN_WORDS = 30


def tokenize(text):
    """Split on whitespace so Bengali and other scripts stay intact."""
    tokens = (w.strip(STRIP_CHARS).lower() for w in text.split())
    return [t for t in tokens if t]


def split_sentences(text):
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def analyze(text):
    words = tokenize(text)
    if len(words) < MIN_WORDS:
        raise ValueError(f"Text too short: need at least {MIN_WORDS} words.")

    lengths = [len(tokenize(s)) for s in split_sentences(text)]
    mean_len = statistics.mean(lengths)
    burstiness = statistics.pstdev(lengths) / mean_len if mean_len else 0.0

    diversity = len(set(words)) / len(words)

    trigrams = list(zip(words, words[1:], words[2:]))
    counts = Counter(trigrams)
    repetition = sum(c for c in counts.values() if c > 1) / len(trigrams)

    flags = []
    if len(lengths) >= 3 and burstiness < LOW_BURSTINESS:
        flags.append("uniform sentence lengths")
    if diversity < LOW_DIVERSITY:
        flags.append("low vocabulary diversity")
    if repetition > HIGH_REPETITION:
        flags.append("repeated phrases")

    return {
        "words": len(words),
        "sentences": len(lengths),
        "sentence_length_variation": round(burstiness, 3),
        "vocabulary_diversity": round(diversity, 3),
        "repeated_phrase_ratio": round(repetition, 3),
        "flags": flags,
        "signals_triggered": f"{len(flags)}/3",
    }


def main():
    parser = argparse.ArgumentParser(description="Experimental text heuristics.")
    parser.add_argument("file", nargs="?", help="Text file (default: stdin)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    try:
        result = analyze(text)
    except ValueError as err:
        sys.exit(str(err))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("DeepShield-Local (experimental heuristics)")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("Note: these are weak signals, not proof of AI-generated text.")


if __name__ == "__main__":
    main()
