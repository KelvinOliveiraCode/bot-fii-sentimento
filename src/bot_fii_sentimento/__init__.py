"""bot-fii-sentimento: sentimento de notícias + sugestão de FIIs (MVP)."""

from .backtest import ResultadoBacktest, executar_backtest
from .coleta import coletar_noticias_sinteticas, coletar_via_yfinance
from .modelo import NewsItem, ResultadoBacktest as _RB, Sugestao
from .sugerir import sugerir_fiis
from .sentimento import analisar_sentimento, classificar

__all__ = [
    "NewsItem",
    "Sugestao",
    "ResultadoBacktest",
    "coletar_noticias_sinteticas",
    "coletar_via_yfinance",
    "analisar_sentimento",
    "classificar",
    "sugerir_fiis",
    "executar_backtest",
]

__version__ = "0.1.0"
