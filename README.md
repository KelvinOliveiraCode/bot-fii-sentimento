# bot-fii-sentimento

Bot de sentimento de notícias com sugestão de FIIs (MVP de IA/ML). Lê notícias, classifica o sentimento com VADER (nltk), agrega o resultado por FII e sugere quais comprar, evitar ou manter neutro. Inclui um backtest simples com preços sintéticos determinísticos.

## Pilha

Python 3.10 ou superior.

- nltk >= 3.8 (VADER; o lexicon está vendido no pacote, então a análise funciona sem rede)
- yfinance >= 0.2 (opcional, requer rede)
- telegram-lite >= 0.1 (opcional, apenas para notificações via Telegram)
- pytest >= 8.0 (dependência de desenvolvimento)

yfinance e telegram-lite são importações guardadas: o pacote roda com apenas nltk instalado, sem qualquer chamada de rede.

## Como usar

Instale o pacote em modo editável:

```
python -m pip install -e .
```

Os testes exigem pytest: instale com `python -m pip install -e .[dev]` ou instale o pytest separadamente.

### Execução offline (padrão)

Rode o pipeline com notícias sintéticas, sem rede:

```
python -m bot_fii_sentimento
```

Ao rodar a partir dos fontes sem instalar o pacote, defina o caminho do pacote:

```
PYTHONPATH=src python -m bot_fii_sentimento
```

Saída observada do programa

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

O programa imprime em português. Os resultados usam notícias sintéticas fixas (random_state 42) e são reproduzíveis.

### Com rede (yfinance)

```
python -m bot_fii_sentimento --rede
```

Coleta notícias reais via yfinance. Falhas de rede ou de ticker são engolidas e o pipeline volta para as notícias sintéticas.

### Telegram

```
python -m bot_fii_sentimento --telegram
```

Envia as sugestões pelo Telegram apenas quando TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID estão definidos e o telegram-lite está instalado. Caso contrário, encerra sem erro.

## Como funciona

1. Coleta: notícias sintéticas determinísticas (cinco FIIs: XPML11.SA, KNRI11.SA, HGLG11.SA, MXRF11.SA, VRTA11.SA) ou notícias reais via yfinance.
2. Sentimento: VADER analisa o texto de cada notícia, com escore compound entre -1 e 1; compound maior ou igual a 0.05 classifica como positivo, menor ou igual a -0.05 classifica como negativo, caso contrário neutro. Como o lexicon é em inglês, textos em português tendem a classificar como neutro.
3. Sugestão: média dos escores por FII, arredondada a quatro casas decimais; score maior ou igual a 0.05 gera "compra", menor ou igual a -0.05 gera "evitar", entre os dois gera "neutro". Ordenado por score decrescente e depois por ticker.
4. Backtest: preços sintéticos determinísticos (random_state 20240101, 60 períodos); compara a carteira igual-peso dos FIIs classificados como "compra" contra um benchmark igual-peso de todos os FIIs com notícias. Retorna o retorno da estratégia, o retorno do benchmark e as vitórias (períodos em que a estratégia igualou ou superou o benchmark).

## Testes

Os testes usam notícias sintéticas, sem rede:

```
python -m pytest -q
```

Espera-se 13 testes aprovados, em 4 módulos de teste.

## Licença

MIT

## Autor

Kelvin Oliveira
