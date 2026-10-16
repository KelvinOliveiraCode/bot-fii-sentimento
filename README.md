# bot-fii-sentimento

## pt-BR

Bot de sentimento de notícias com sugestão de FIIs (MVP de IA/ML). Lê notícias, classifica o sentimento com VADER (nltk), agrega o resultado por FII e sugere quais comprar, evitar ou manter neutro. Inclui um backtest simples com preços sintéticos determinísticos.

Pilha: Python 3.10+, nltk (VADER), yfinance, telegram-lite, pytest.

### Como usar

Instale o pacote:

```
python -m pip install -e .
```

Para rodar offline, basta `python -m pip install nltk`; yfinance e telegram-lite são importações opcionais e o código funciona sem eles.

Execute o pipeline com notícias sintéticas (sem rede):

```
python -m bot_fii_sentimento
```

Exemplo de saída:

```
=== bot-fii-sentimento ===
Notícias analisadas: 5

Sugestões de FIIs:
  XPML11.SA: score=0.4400 (compra) — 1 notícia(s)
  HGLG11.SA: score=0.2100 (compra) — 1 notícia(s)
  MXRF11.SA: score=0.0000 (neutro) — 1 notícia(s)
  VRTA11.SA: score=-0.3400 (evitar) — 1 notícia(s)
  KNRI11.SA: score=-0.4200 (evitar) — 1 notícia(s)

Backtest:
  Estratégia: 0.12%
  Benchmark:  0.08%
  Vitórias: 30/59
```

Use yfinance (requer rede):

```
python -m bot_fii_sentimento --rede
```

Envie sugestões pelo Telegram (apenas se TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID estiverem definidos):

```
python -m bot_fii_sentimento --telegram
```

### Testes

Os testes usam notícias sintéticas, sem rede:

```
python -m pytest -q
```

Resultado esperado: 13 passed.

### Licença

MIT

### Autor

Kelvin Oliveira

---

## English

News sentiment bot with FII suggestions (AI/ML MVP). Reads news, classifies sentiment with VADER (nltk), aggregates by FII, and suggests which to buy, avoid, or keep neutral. Includes a simple backtest with deterministic synthetic prices.

Stack: Python 3.10+, nltk (VADER), yfinance, telegram-lite, pytest.

### How to use

Install the package:

```
python -m pip install -e .
```

To run offline, `python -m pip install nltk` is enough; yfinance and telegram-lite are optional imports and the code works without them.

Run the pipeline with synthetic news (no network):

```
python -m bot_fii_sentimento
```

Example output:

```
=== bot-fii-sentimento ===
Notícias analisadas: 5

Sugestões de FIIs:
  XPML11.SA: score=0.4400 (compra) — 1 notícia(s)
  HGLG11.SA: score=0.2100 (compra) — 1 notícia(s)
  MXRF11.SA: score=0.0000 (neutro) — 1 notícia(s)
  VRTA11.SA: score=-0.3400 (evitar) — 1 notícia(s)
  KNRI11.SA: score=-0.4200 (evitar) — 1 notícia(s)

Backtest:
  Estratégia: 0.12%
  Benchmark:  0.08%
  Vitórias: 30/59
```

Use yfinance (requires network):

```
python -m bot_fii_sentimento --rede
```

Send suggestions via Telegram (only if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set):

```
python -m bot_fii_sentimento --telegram
```

### Tests

Tests use synthetic news, no network:

```
python -m pytest -q
```

Expected result: 13 passed.

### License

MIT

### Author

Kelvin Oliveira
