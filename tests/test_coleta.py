"""Testes da coleta de notícias (apenas sintética, sem rede)."""

from datetime import datetime

from bot_fii_sentimento.coleta import coletar_noticias_sinteticas
from bot_fii_sentimento.modelo import NewsItem


def test_coletar_noticias_sinteticas_retorna_lista_de_newsitem():
    noticias = coletar_noticias_sinteticas()
    assert isinstance(noticias, list)
    assert len(noticias) == 5
    for item in noticias:
        assert isinstance(item, NewsItem)
        assert item.fii is not None
        assert item.source == "sintetico"


def test_coletar_noticias_sinteticas_eh_deterministico():
    primeira = coletar_noticias_sinteticas(random_state=42)
    segunda = coletar_noticias_sinteticas(random_state=42)
    assert [item.title for item in primeira] == [item.title for item in segunda]


def test_coletar_noticias_sinteticas_datas_sao_iso():
    for item in coletar_noticias_sinteticas():
        datetime.fromisoformat(item.date)  # levanta se não for ISO 8601
