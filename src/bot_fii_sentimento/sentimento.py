"""Análise de sentimento de notícias com VADER (nltk).

O lexicon VADER é vendido no pacote (``src/bot_fii_sentimento/data``) para
que a análise funcione sem rede, sem depender de ``nltk.download``.
"""

from __future__ import annotations

from typing import Dict, Optional

from pathlib import Path

import nltk  # type: ignore[import-not-found]
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # type: ignore[import-not-found]

from .modelo import NewsItem

# Caminho do lexicon vendido dentro do pacote.
_DIRETORIO_DADOS = Path(__file__).resolve().parent / "data"
if str(_DIRETORIO_DADOS) not in nltk.data.path:  # type: ignore[attr-defined]
    nltk.data.path.append(str(_DIRETORIO_DADOS))  # type: ignore[attr-defined]

# Limiares fixos (determinísticos) para classificação.
LIMIAR_POSITIVO = 0.05
LIMIAR_NEGATIVO = -0.05

_analisador: Optional[SentimentIntensityAnalyzer] = None


def _obter_analisador() -> SentimentIntensityAnalyzer:
    global _analisador
    if _analisador is None:
        try:
            _analisador = SentimentIntensityAnalyzer()
        except LookupError:  # pragma: no cover - lexicon está vendido
            import nltk as _nltk  # type: ignore[import-not-found]

            _nltk.download("vader_lexicon", quiet=True)
            _analisador = SentimentIntensityAnalyzer()
    return _analisador


def analisar_sentimento(texto: str) -> Dict[str, float]:
    """Retorna os escores de VADER (compound, pos, neu, neg) para o texto."""
    if not texto:
        return {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
    analisador = _obter_analisador()
    return analisador.polarity_scores(texto)


def classificar(compound: float) -> str:
    """Classifica um escore compound em positivo / negativo / neutro."""
    if compound >= LIMIAR_POSITIVO:
        return "positivo"
    if compound <= LIMIAR_NEGATIVO:
        return "negativo"
    return "neutro"


def sentimento_da_noticia(item: NewsItem) -> Dict[str, object]:
    """Analisa o sentimento de uma NewsItem e retorna um dicionário enriquecido."""
    pontuacao = analisar_sentimento(item.text)
    return {
        "fii": item.fii,
        "title": item.title,
        "compound": pontuacao["compound"],
        "classificacao": classificar(pontuacao["compound"]),
    }
