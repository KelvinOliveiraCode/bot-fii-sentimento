"""Modelos de dados do bot-fii-sentimento."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class NewsItem:
    """Uma notícia coletada.

    Attributes:
        title: Título da notícia.
        text: Texto (ou resumo) usado na análise de sentimento.
        date: Data da notícia em ISO 8601 (YYYY-MM-DD).
        source: Fonte da notícia (ex.: "sintetico", "yfinance").
        fii: Ticker do FII relacionado, se houver.
    """

    title: str
    text: str
    date: str
    source: str
    fii: Optional[str] = None

    def __post_init__(self) -> None:
        try:
            datetime.fromisoformat(self.date)
        except ValueError as exc:  # pragma: no cover - dados sintéticos são válidos
            raise ValueError(f"Data inválida (esperado ISO 8601): {self.date!r}") from exc


@dataclass(frozen=True)
class Sugestao:
    """Sugestão de FII derivada do sentimento agregado.

    Attributes:
        fii: Ticker do FII.
        score: Score agregado de sentimento (média dos compostos).
        noticias: Quantidade de notícias do FII usadas.
        classificacao: "compra", "neutro" ou "evitar".
    """

    fii: str
    score: float
    noticias: int
    classificacao: str


@dataclass(frozen=True)
class ResultadoBacktest:
    """Resultado do backtest simples.

    Attributes:
        retorno_estrategia: Retorno médio da carteira dos FIIs sugeridos.
        retorno_benchmark: Retorno médio do benchmark (igual-peso).
        vitorias: Períodos em que a estratégia igualou ou superou o benchmark.
        total_periodos: Total de períodos simulados.
    """

    retorno_estrategia: float
    retorno_benchmark: float
    vitorias: int
    total_periodos: int

    @property
    def bateu_benchmark(self) -> bool:
        """True quando a estratégia não ficou pior que o benchmark."""
        return self.retorno_estrategia >= self.retorno_benchmark
