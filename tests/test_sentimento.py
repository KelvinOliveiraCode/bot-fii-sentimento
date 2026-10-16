"""Testes da análise de sentimento VADER."""

from bot_fii_sentimento.sentimento import analisar_sentimento, classificar


def test_analisar_sentimento_retorna_chaves_esperadas():
    pontuacao = analisar_sentimento("Boa notícia de dividendos")
    assert set(pontuacao) == {"compound", "pos", "neu", "neg"}
    assert -1.0 <= pontuacao["compound"] <= 1.0
    for chave in ("pos", "neu", "neg"):
        assert 0.0 <= pontuacao[chave] <= 1.0


def test_classificar_limiares():
    assert classificar(0.05) == "positivo"
    assert classificar(0.06) == "positivo"
    assert classificar(-0.05) == "negativo"
    assert classificar(-0.06) == "negativo"
    assert classificar(0.0) == "neutro"
    assert classificar(0.04) == "neutro"
    assert classificar(-0.04) == "neutro"


def test_analisar_sentimento_texto_vazio():
    pontuacao = analisar_sentimento("")
    assert pontuacao == {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
