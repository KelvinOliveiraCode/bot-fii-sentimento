"""Testes da sugestão de FIIs."""

from bot_fii_sentimento.coleta import coletar_noticias_sinteticas
from bot_fii_sentimento.sugerir import sugerir_fiis


def test_sugerir_fiis_ordena_por_score_decrescente():
    noticias = coletar_noticias_sinteticas(random_state=42)
    sugestoes = sugerir_fiis(noticias)
    scores = [sugestao.score for sugestao in sugestoes]
    assert scores == sorted(scores, reverse=True)


def test_sugerir_fiis_estrutura():
    noticias = coletar_noticias_sinteticas(random_state=42)
    sugestoes = sugerir_fiis(noticias)
    assert len(sugestoes) == 5
    for sugestao in sugestoes:
        assert sugestao.fii
        assert isinstance(sugestao.score, float)
        assert isinstance(sugestao.noticias, int)
        assert sugestao.classificacao in ("compra", "neutro", "evitar")


def test_sugerir_fiis_vazio_retorna_vazio():
    assert sugerir_fiis([]) == []


def test_sugerir_fiis_eh_deterministico():
    noticias = coletar_noticias_sinteticas(random_state=7)
    assert sugerir_fiis(noticias) == sugerir_fiis(list(noticias))
