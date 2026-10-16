"""Backtest simples da estratégia de sugestão de FIIs.

Usa preços sintéticos determinísticos (sem rede), gerados com ``random_state``
fixo, para comparar a carteira dos FIIs sugeridos contra um benchmark.
"""

from __future__ import annotations

import random
from typing import List

from .modelo import NewsItem, ResultadoBacktest
from .sugerir import sugerir_fiis

SEED_BACKTEST = 20240101


def _gerar_precos(
    fiis: List[str], periodo: int = 60, random_state: int = SEED_BACKTEST
) -> dict[str, List[float]]:
    """Gera série de preços sintética e determinística (sem rede)."""
    rng = random.Random(random_state)
    precos: dict[str, List[float]] = {}
    for fii in fiis:
        preco = 100.0
        serie = [preco]
        for _ in range(periodo - 1):
            preco = max(1.0, preco * (1 + rng.gauss(0.0, 0.01)))
            serie.append(round(preco, 4))
        precos[fii] = serie
    return precos


def executar_backtest(
    noticias: List[NewsItem],
    min_noticias: int = 1,
    periodo: int = 60,
    random_state: int = SEED_BACKTEST,
) -> ResultadoBacktest:
    """Executa backtest simples.

    Compara a carteira dos FIIs classificados como "compra" (pesos iguais)
    contra um benchmark de igual-peso sobre todos os FIIs com notícias, usando
    preços sintéticos determinísticos. Retorna ResultadoBacktest.
    """
    sugestoes = sugerir_fiis(noticias, min_noticias=min_noticias)
    fiis_estrategia = [s.fii for s in sugestoes if s.classificacao == "compra"]
    todos_fiis = sorted({n.fii for n in noticias if n.fii})
    if not todos_fiis:
        return ResultadoBacktest(0.0, 0.0, 0, 0)
    if not fiis_estrategia:
        fiis_estrategia = list(todos_fiis)

    precos = _gerar_precos(todos_fiis, periodo=periodo, random_state=random_state)

    # Retornos perioduais por ativo.
    retornos_periodo: dict[str, List[float]] = {}
    for fii in todos_fiis:
        serie = precos[fii]
        retornos_periodo[fii] = [
            (serie[i + 1] - serie[i]) / serie[i] for i in range(periodo - 1)
        ]

    def media_retorno(ativos: List[str], indice_periodo: int) -> float:
        valores = [retornos_periodo[a][indice_periodo] for a in ativos]
        return sum(valores) / len(valores)

    retorno_estrategia = sum(
        media_retorno(fiis_estrategia, i) for i in range(periodo - 1)
    ) / (periodo - 1)
    retorno_benchmark = sum(
        media_retorno(todos_fiis, i) for i in range(periodo - 1)
    ) / (periodo - 1)

    vitorias = sum(
        1
        for i in range(periodo - 1)
        if media_retorno(fiis_estrategia, i) >= media_retorno(todos_fiis, i)
    )

    return ResultadoBacktest(
        retorno_estrategia=round(retorno_estrategia, 4),
        retorno_benchmark=round(retorno_benchmark, 4),
        vitorias=vitorias,
        total_periodos=periodo - 1,
    )
