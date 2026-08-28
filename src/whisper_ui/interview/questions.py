from __future__ import annotations

import re
from dataclasses import dataclass

from whisper_ui.interview.roles import RoleTurn


@dataclass
class InterviewQuestion:
    start: float
    end: float
    text: str


QUESTION_STARTS = (
    "кто ",
    "что ",
    "где ",
    "куда ",
    "откуда ",
    "когда ",
    "почему ",
    "зачем ",
    "как ",
    "какой ",
    "какая ",
    "какие ",
    "какое ",
    "сколько ",
    "чем ",
    "чего ",
    "кому ",
    "можете ",
    "можешь ",
    "готовы ",
    "готов ",
    "расскажите ",
    "расскажи ",
    "объясните ",
    "объясни ",
)


def is_question(text: str) -> bool:
    normalized = text.strip().lower()

    if not normalized:
        return False

    # Комментарии: если Whisper поставил знак вопроса —
    # Комментарии: считаем предложение вопросом напрямую.
    if normalized.endswith("?"):
        return True

    # Комментарии: Whisper иногда ошибается с пунктуацией.
    # Комментарии: поэтому дополнительно проверяем характерные
    # Комментарии: начала вопросительных фраз.
    return normalized.startswith(QUESTION_STARTS)


def extract_interviewer_questions(
    turns: list[RoleTurn],
) -> list[InterviewQuestion]:
    questions: list[InterviewQuestion] = []

    for turn in turns:
        if turn.role != "INTERVIEWER":
            continue

        # Комментарии: разбиваем длинную реплику интервьюера
        # Комментарии: на отдельные предложения.
        sentences = re.split(r"(?<=[.!?])\s+", turn.text)

        for sentence in sentences:
            sentence = sentence.strip()

            if not is_question(sentence):
                continue

            questions.append(
                InterviewQuestion(
                    start=turn.start,
                    end=turn.end,
                    text=sentence,
                )
            )

    return questions
