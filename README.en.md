# bot-fii-sentimento

News sentiment bot with FII suggestions (AI/ML MVP). Reads news, classifies sentiment with VADER (nltk), aggregates the result by FII, and suggests which to buy, avoid, or keep neutral. Includes a simple backtest with deterministic synthetic prices.

## Stack

Python 3.10 or newer.

- nltk >= 3.8 (VADER; the lexicon is vendored in the package, so analysis works offline)
- yfinance >= 0.2 (optional, requires network)
- telegram-lite >= 0.1 (optional, Telegram notifications only)
- pytest >= 8.0 (development dependency)

yfinance and telegram-lite are guarded optional imports: the package runs with only nltk installed and makes no network calls.

## How to use

Install the package in editable mode:

```
python -m pip install -e .
```

Tests require pytest: install with `python -m pip install -e .[dev]` or install pytest separately.

### Offline run (default)

Run the pipeline with synthetic news, no network:

```
python -m bot_fii_sentimento
```

When running from the sources without installing the package, set the package path:

```
PYTHONPATH=src python -m bot_fii_sentimento
```

Observed program output

```
=== bot-fii-sentimento ===
Notícias analisadas: 5

Sugestões de FIIs:
  HGLG11.SA: score=0.000 (neutro) — 1 notícia(s)
  KNRI11.SA: score=0.000 (neutro) — 1 notícia(s)
  MXRF11.SA: score=0.000 (neutro) — 1 notícia(s)
  VRTA11.SA: score=0.000 (neutro) — 1 notícia(s)
  XPML11.SA: score=0.000 (neutro) — 1 notícia(s)

Backtest:
  Estratégia: -0.03%
  Benchmark:  -0.03%
  Vitórias: 59/59
```

The program prints in Portuguese. Results use fixed synthetic news (random_state 42) and are reproducible.

### Network run (yfinance)

```
python -m bot_fii_sentimento --rede
```

Collects real news via yfinance. Network or ticker failures are swallowed and the pipeline falls back to the synthetic news.

### Telegram

```
python -m bot_fii_sentimento --telegram
```

Sends the suggestions via Telegram only when TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are defined and telegram-lite is installed. Otherwise it exits without error.

## How it works

1. Collection: deterministic synthetic news (five FIIs: XPML11.SA, KNRI11.SA, HGLG11.SA, MXRF11.SA, VRTA11.SA) or real news via yfinance.
2. Sentiment: VADER analyzes each news text, with compound score between -1 and 1; compound greater than or equal to 0.05 classifies as positive, less than or equal to -0.05 classifies as negative, otherwise neutral. Since the lexicon is English, Portuguese texts tend to classify as neutral.
3. Suggestion: average score per FII, rounded to four decimal places; score greater than or equal to 0.05 yields "compra", less than or equal to -0.05 yields "evitar", in between yields "neutro". Sorted by descending score, then by ticker.
4. Backtest: deterministic synthetic prices (random_state 20240101, 60 periods); compares the equal-weight portfolio of FIIs classified as "compra" against an equal-weight benchmark of all FIIs with news. Returns the strategy return, the benchmark return, and the wins (periods in which the strategy matched or beat the benchmark).

## Tests

Tests use synthetic news, no network:

```
python -m pytest -q
```

Expects 13 passed tests, in 4 test modules.

## License

MIT

## Author

Kelvin Oliveira
