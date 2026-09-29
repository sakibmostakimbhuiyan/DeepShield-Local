# 🛡️ DeepShield-Local: Text Heuristics for Local-Language Content

> An early-stage, experimental Python tool that measures simple statistical signals in text (including Bengali) to explore how synthetic or manipulated content might be flagged in local languages.

![Status](https://img.shields.io/badge/status-early%20prototype-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Motivation

Most AI-content detection research targets major international languages. Local languages such as Bengali get far less attention, which leaves communities more exposed to misinformation. DeepShield-Local is a small first step toward exploring this gap.

## ⚠️ What This Is (and Is Not)

This is **not** a trained deepfake or AI-text detector, and it cannot prove that any text is machine-generated. It computes a few weak statistical signals and reports which ones look unusual. The thresholds are illustrative and have not been calibrated on real datasets. Treat the output as a starting point for investigation, never as a verdict.

## ⚙️ How It Works

The script reads a text file and computes three signals:

| Signal | What it measures |
|---|---|
| Sentence-length variation | How much sentence lengths differ (very uniform text is flagged) |
| Vocabulary diversity | Ratio of unique words to total words |
| Repeated-phrase ratio | Share of three-word phrases that repeat |

Words are split on whitespace, so Bengali and other scripts are handled without language-specific libraries.

## 🚀 Usage

```bash
git clone https://github.com/sakibmostakimbhuiyan/DeepShield-Local.git
cd DeepShield-Local
python3 src/analyze.py samples/sample_en.txt
python3 src/analyze.py samples/sample_en.txt --json
python3 -m unittest tests/test_analyze.py
```

Requires Python 3.8+ and no external packages.

## 🗂️ Project Structure

```
src/        analysis script
tests/      unit tests
samples/    example input
```

## 🗺️ Roadmap

- [x] Basic text-statistics script with tests
- [ ] Collect and label a small Bengali text dataset
- [ ] Calibrate thresholds against real data and report accuracy honestly
- [ ] Add audio feature extraction
- [ ] Evaluate limitations and failure cases in a written report

## 📄 License

MIT License. See [LICENSE](LICENSE).

## 👤 Author

**Sakib Mostakim Bhuiyan** · [GitHub](https://github.com/sakibmostakimbhuiyan)
