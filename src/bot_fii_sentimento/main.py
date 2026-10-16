"""Ponto de entrada do bot-fii-sentimento.

Pipeline: coleta de notícias → análise de sentimento (VADER) → sugestão de FIIs
→ backtest simples. Por padrão usa notícias sintéticas (sem rede).
"""

from __future__ import annotations

import argparse

from .backtest import executar_backtest
from .coleta import coletar_noticias_sinteticas, coletar_via_yfinance
from .notificacao import enviar_sugestoes
from .sugerir import sugerir_fiis


def executar(usar_rede: bool = False, enviar_telegram: bool = False) -> None:
    """Executa o pipeline completo e imprime o resultado."""
    if usar_rede:
        noticias = coletar_via_yfinance()
        if not noticias:
            noticias = coletar_noticias_sinteticas()
    else:
        noticias = coletar_noticias_sinteticas()

    sugestoes = sugerir_fiis(noticias)
    resultado = executar_backtest(noticias)

    print("=== bot-fii-sentimento ===")
    print(f"Notícias analisadas: {len(noticias)}")
    print("\nSugestões de FIIs:")
    for sugestao in sugestoes:
        print(
            f"  {sugestao.fii}: score={sugestao.score:.3f} "
            f"({sugestao.classificacao}) — {sugestao.noticias} notícia(s)"
        )
    print("\nBacktest:")
    print(f"  Estratégia: {resultado.retorno_estrategia:.2%}")
    print(f"  Benchmark:  {resultado.retorno_benchmark:.2%}")
    print(f"  Vitórias: {resultado.vitorias}/{resultado.total_periodos}")

    if enviar_telegram:
        enviado = enviar_sugestoes(sugestoes)
        print(f"\nTelegram: {'enviado' if enviado else 'não configurado/offline'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="bot-fii-sentimento")
    parser.add_argument(
        "--rede",
        action="store_true",
        help="usar yfinance (requer rede); fallback para sintético",
    )
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="enviar sugestões pelo Telegram se configurado",
    )
    args = parser.parse_args()
    executar(usar_rede=args.rede, enviar_telegram=args.telegram)


if __name__ == "__main__":
    main()
