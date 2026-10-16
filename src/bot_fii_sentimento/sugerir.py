"""Sugestão de FIIs a partir do sentimento agregado das notícias."""

from __future__ import annotations

from typing import List

from .modelo import NewsItem, Sugestao
from .sentimento import LIMIAR_NEGATIVO, LIMIAR_POSITIVO, analisar_sentimento


def sugerir_fiis(noticias: List[NewsItem], min_noticias: int = 1) -> List[Sugestao]:
    """Sugere FIIs ordenados pelo score agregado de sentimento.

    Args:
        noticias: Lista de notícias já coletadas.
        min_noticias: Quantidade mínima de notícias para o FII entrar na lista.

    Returns:
        Lista de Sugestao ordenada por score desc (e depois por ticker).
        É determinística: mesma entrada produz sempre a mesma saída.
    """
    totais: dict[str, float] = {}
    contagens: dict[str, int] = {}
    for item in noticias:
        if not item.fii:
            continue
        compound = analisar_sentimento(item.text)["compound"]
        totais[item.fii] = totais.get(item.fii, 0.0) + compound
        contagens[item.fii] = contagens.get(item.fii, 0) + 1

    sugestoes: List[Sugestao] = []
    for fii, total in totais.items():
        qtd = contagens[fii]
        if qtd < min_noticias:
            continue
        score = round(total / qtd, 4)
        if score >= LIMIAR_POSITIVO:
            classificacao = "compra"
        elif score <= LIMIAR_NEGATIVO:
            classificacao = "evitar"
        else:
            classificacao = "neutro"
        sugestoes.append(
            Sugestao(
                fii=fii,
                score=score,
                noticias=qtd,
                classificacao=classificacao,
            )
        )

    sugestoes.sort(key=lambda sugestao: (-sugestao.score, sugestao.fii))
    return sugestoes

