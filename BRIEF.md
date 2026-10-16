# BRIEF — bot-fii-sentimento

Projeto: bot-fii-sentimento (área IA/ML — sentimento de notícias + sugestão de FIIs).
Local: C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\bot-fii-sentimento\
Autor: Kelvin Oliveira
Licença: MIT

## Entregas

- pyproject.toml — metadados, dependências, entry point e config do pytest (pythonpath = src).
- src/bot_fii_sentimento/ — pacote:
  - __init__.py, modelo.py (NewsItem, Sugestao, ResultadoBacktest)
  - coleta.py (notícias sintéticas determinísticas + yfinance opcional sem falhar offline)
  - sentimento.py (VADER com lexicon vendido; funciona sem rede)
  - sugerir.py (agregação por FII, sugestão compra/neutro/evitar)
  - backtest.py (backtest simples, preços sintéticos, random_state fixo)
  - notificacao.py (telegram-lite opcional, só se houver token/chat)
  - main.py (CLI: --rede, --telegram)
- tests/ — 4 módulos, 13 testes, notícias sintéticas, sem rede.
- README.md — bilíngue PT-BR + EN (título, descrição, como usar, testes, licença, autor).
- BRIEF.md — este arquivo.

## Critérios de aceitação (MVP)

- [x] Coleta de notícias (sintética determinística; yfinance opcional).
- [x] Análise de sentimento com VADER (nltk).
- [x] Sugestão de FIIs agregada por sentimento.
- [x] Backtest simples com preços sintéticos determinísticos.
- [x] Testes que passam (sem rede).
- [x] README bilíngue PT-BR + EN completo.

## Como verificar

```
cd C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\bot-fii-sentimento
python -m pytest -q
```

Comando de teste: `python -m pytest -q`
Resultado esperado: `13 passed` (suite verde).
Resultado obtido: `13 passed in 6.05s`.

Também:

```
python -m bot_fii_sentimento
```
Deve imprimir sugestões de FIIs e backtest sem erro e sem rede.

## Observação de design

yfinance e telegram-lite estão listados na pilha e no pyproject.toml, mas são importações guardadas: o pacote roda com apenas nltk instalado, sem rede.
