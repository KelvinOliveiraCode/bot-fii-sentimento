"""Testes do backtest simples (preços sintéticos, sem rede)."""

from bot_fii_sentimento.backtest import executar_backtest
from bot_fii_sentimento.coleta import coletar_noticias_sinteticas
from bot_fii_sentimento.modelo import ResultadoBacktest


def test_executar_backtest_retorna_estrutura():
    noticias = coletar_noticias_sinteticas(random_state=42)
    resultado = executar_backtest(noticias)
    assert isinstance(resultado, ResultadoBacktest)
    assert -1.0 <= resultado.retorno_estrategia <= 1.0
    assert -1.0 <= resultado.retorno_benchmark <= 1.0
    assert 0 <= resultado.vitorias <= resultado.total_periodos
    assert resultado.total_periodos > 0


def test_executar_backtest_eh_deterministico():
    noticias = coletar_noticias_sinteticas(random_state=3)
    primeiro = executar_backtest(noticias, random_state=20240101)
    segundo = executar_backtest(noticias, random_state=20240101)
    assert primeiro == segundo


def test_executar_backtest_sem_noticias_retorna_zeros():
    assert executar_backtest([]) == ResultadoBacktest(0.0, 0.0, 0, 0)
