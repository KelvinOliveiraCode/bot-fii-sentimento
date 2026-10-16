"""Coleta de notícias para o bot-fii-sentimento.

Fornece uma fonte sintética determinística (sem rede, para testes e demo)
e uma coleta real opcional via yfinance (requer rede e o pacote instalado).
A coleta real nunca levanta exceção: falhas são engolidas e retornam lista vazia.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import List, Optional

from .modelo import NewsItem

FIIS_PADRAO = ("XPML11.SA", "KNRI11.SA", "HGLG11.SA", "MXRF11.SA", "VRTA11.SA")

_NOTICIAS_SINTETICAS: tuple[dict, ...] = (
    {
        "title": "FII XPML11 anuncia aumento de dividendos no trimestre",
        "text": "O fundo XPML11 distribuiu dividendos acima do esperado este trimestre, com alta na ocupação dos imóveis.",
        "date": "2024-01-10",
        "source": "sintetico",
        "fii": "XPML11.SA",
    },
    {
        "title": "KNRI11 enfrenta vacância elevada em galpões logísticos",
        "text": "O KNRI11 reportou taxa de vacância acima da média nos galpões logísticos, pressionando os rendimentos.",
        "date": "2024-01-11",
        "source": "sintetico",
        "fii": "KNRI11.SA",
    },
    {
        "title": "HGLG11 negocia aquisição de novo ativo corporativo",
        "text": "O HGLG11 está em negociação avançada para comprar um prédio corporativo em São Paulo.",
        "date": "2024-01-12",
        "source": "sintetico",
        "fii": "HGLG11.SA",
    },
    {
        "title": "MXRF11 mantém carteira diversificada e rendimento estável",
        "text": "O MXRF11 segue com rendimento estável e carteira bem diversificada entre setores.",
        "date": "2024-01-13",
        "source": "sintetico",
        "fii": "MXRF11.SA",
    },
    {
        "title": "VRTA11 tem inadimplência de um inquilino grande",
        "text": "O VRTA11 comunicou inadimplência de um inquilino relevante, afetando parcialmente o dividendo.",
        "date": "2024-01-14",
        "source": "sintetico",
        "fii": "VRTA11.SA",
    },
)


def coletar_noticias_sinteticas(random_state: int = 42) -> List[NewsItem]:
    """Retorna notícias sintéticas embaralhadas de forma determinística.

    O mesmo ``random_state`` produz sempre a mesma ordem, o que torna os
    testes e a demo reprodutíveis sem qualquer chamada de rede.
    """
    rng = random.Random(random_state)
    items = [NewsItem(**noticia) for noticia in _NOTICIAS_SINTETICAS]
    rng.shuffle(items)
    return items


def _ts_para_iso(valor: object) -> str:
    """Converte um timestamp Unix (yfinance) ou string para ISO 8601."""
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return datetime.fromtimestamp(float(valor), tz=timezone.utc).date().isoformat()
    texto = str(valor)
    try:
        return datetime.fromisoformat(texto).date().isoformat()
    except ValueError:
        return texto


def coletar_via_yfinance(tickers: Optional[List[str]] = None) -> List[NewsItem]:
    """Coleta notícias reais via yfinance.

    Retorna lista vazia se yfinance não estiver instalado, sem rede ou houver
    falha em algum ticker — nunca levanta exceção, mantendo o MVP robusto
    mesmo offline.
    """
    try:
        import yfinance as yf  # type: ignore[import-not-found]
    except ImportError:
        return []

    tickers = tickers or list(FIIS_PADRAO)
    noticias: List[NewsItem] = []
    for ticker in tickers:
        try:
            objeto = yf.Ticker(ticker)
            news = getattr(objeto, "news", None) or []
            for item in news:
                noticias.append(
                    NewsItem(
                        title=str(item.get("title", "")),
                        text=str(item.get("summary", item.get("title", ""))),
                        date=_ts_para_iso(item.get("providerPublishTime", "")),
                        source="yfinance",
                        fii=ticker,
                    )
                )
        except Exception:
            continue
    return noticias
