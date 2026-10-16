"""Notificação opcional via telegram-lite.

Apenas envia quando TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID estão definidos e o
pacote telegram-lite está instalado. Caso contrário, retorna False silenciosamente
— não há obrigação de rede nem de token para o MVP funcionar.
"""

from __future__ import annotations

import os
from typing import List

from .modelo import Sugestao


def formatar_mensagem(sugestoes: List[Sugestao]) -> str:
    """Formata as sugestões em texto para o Telegram."""
    linhas = ["*Sugestões de FIIs — bot-fii-sentimento*\n"]
    for sugestao in sugestoes[:5]:
        linhas.append(
            f"• {sugestao.fii}: {sugestao.classificacao} (score {sugestao.score:.2f})"
        )
    return "\n".join(linhas)


def enviar_sugestoes(sugestoes: List[Sugestao]) -> bool:
    """Tenta enviar sugestões pelo Telegram; retorna False sem falhar se não houver config."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False
    try:
        import telegram_lite  # type: ignore[import-not-found]
    except ImportError:
        return False
    try:
        bot = telegram_lite.Bot(token)
        bot.send_message(chat_id=chat_id, text=formatar_mensagem(sugestoes))
        return True
    except Exception:
        return False
