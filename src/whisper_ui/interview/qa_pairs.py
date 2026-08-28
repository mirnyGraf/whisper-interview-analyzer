from __future__ import annotations

from dataclasses import dataclass

from whisper_ui.interview.roles import RoleTurn
from whisper_ui.interview.questions import is_question


@dataclass
class QuestionAnswerPair:
    question: str
    answer: str
    question_start: float
    answer_start: float | None


def extract_qa_pairs(
    turns: list[RoleTurn],
) -> list[QuestionAnswerPair]:
    pairs: list[QuestionAnswerPair] = []

    for index, turn in enumerate(turns):

        # Комментарии: рассматриваем только реплики интервьюера.
        if turn.role != "INTERVIEWER":
            continue

        # Комментарии: пока берём всю реплику интервьюера как потенциальный вопрос,
        # Комментарии: но сначала проверяем, есть ли в ней вопросительная часть.
        sentences = [
            sentence.strip()
            for sentence in turn.text.replace("!", ".").split(".")
            if sentence.strip()
        ]

        question_sentences = [
            sentence
            for sentence in sentences
            if is_question(sentence)
        ]

        if not question_sentences:
            continue

        question = " ".join(question_sentences)

        answer_parts: list[str] = []
        answer_start: float | None = None

        # Комментарии: после вопроса ищем следующие реплики кандидата.
        # Комментарии: собираем их до следующей реплики интервьюера.
        for next_turn in turns[index + 1:]:

            if next_turn.role == "INTERVIEWER":
                break

            if next_turn.role == "CANDIDATE":
                if answer_start is None:
                    answer_start = next_turn.start

                answer_parts.append(next_turn.text)

        pairs.append(
            QuestionAnswerPair(
                question=question,
                answer=" ".join(answer_parts),
                question_start=turn.start,
                answer_start=answer_start,
            )
        )

    return pairs
