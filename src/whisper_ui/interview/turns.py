from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DialogueTurn:
    speaker: str
    start: float
    end: float
    text: str


def merge_segments_into_turns(
    segments: list[dict[str, Any]],
) -> list[DialogueTurn]:
    """Объединяет соседние сегменты одного спикера в одну реплику."""

    turns: list[DialogueTurn] = []

    for segment in segments:
        speaker = segment.get("speaker")
        text = str(segment.get("text", "")).strip()

        # Комментарии: сегменты без текста или без спикера нам для анализа не нужны.
        if not speaker or not text:
            continue

        start = float(segment.get("start", 0.0))
        end = float(segment.get("end", start))

        # Комментарии: если предыдущая реплика принадлежит тому же спикеру,
        # Комментарии: продолжаем её, а не создаём новую.
        if turns and turns[-1].speaker == speaker:
            turns[-1].end = end
            turns[-1].text = f"{turns[-1].text} {text}"
            continue

        # Комментарии: сменился спикер — начинаем новую реплику.
        turns.append(
            DialogueTurn(
                speaker=speaker,
                start=start,
                end=end,
                text=text,
            )
        )

    return turns
