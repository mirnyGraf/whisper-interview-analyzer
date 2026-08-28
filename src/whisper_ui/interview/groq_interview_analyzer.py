from __future__ import annotations

import json
from dataclasses import dataclass

from whisper_ui.interview.groq_client import GroqClient
from whisper_ui.interview.roles import RoleTurn


@dataclass
class InterviewQA:
    question: str
    candidate_answer: str
    relevant: bool


SYSTEM_PROMPT =SYSTEM_PROMPT = """
Ты анализируешь полную расшифровку собеседования.

Роли уже определены:

INTERVIEWER — интервьюер.
CANDIDATE — кандидат.

Твоя задача — извлечь ТОЛЬКО содержательные вопросы,
которые INTERVIEWER задаёт CANDIDATE для оценки его
профессиональных качеств.

Возвращай вопрос только если он проверяет или раскрывает:

- профессиональные знания;
- технические знания;
- профессиональный опыт;
- навыки;
- архитектурное мышление;
- решение рабочих задач;
- поведение в рабочих ситуациях;
- понимание технологий;
- причины профессиональных решений.

НЕ возвращай:

- вопросы кандидата работодателю;
- вопросы о зарплате;
- вопросы о графике;
- вопросы о ГСМ;
- вопросы о дороге;
- вопросы о документах;
- вопросы об условиях работы;
- бытовые вопросы;
- организационные вопросы;
- риторические вопросы;
- случайные фразы, ошибочно распознанные как вопросы.

Если один вопрос повторяется или переформулируется,
верни его только один раз.

Для каждого найденного вопроса:

1. Сформулируй чистую формулировку вопроса.
2. Найди фактический ответ CANDIDATE по смыслу.
3. Не придумывай ответ.
4. Если кандидат не ответил, candidate_answer = "".

Не добавляй вопросы только ради заполнения результата.

Если содержательных вопросов интервьюера в разговоре нет,
верни пустой список.

Верни только JSON:

{
  "items": [
    {
      "question": "...",
      "candidate_answer": "...",
      "relevant": true
    }
  ]
}
"""


def analyze_interview(
    turns: list[RoleTurn],
    *,
    client: GroqClient,
) -> list[InterviewQA]:

    dialogue = "\n".join(
        f"{turn.role}: {turn.text}"
        for turn in turns
    )

    raw = client.chat(
        system=SYSTEM_PROMPT,
        user=f"ДИАЛОГ:\n{dialogue}",
    )

    data = json.loads(raw)

    return [
        InterviewQA(
            question=str(item.get("question", "")).strip(),
            candidate_answer=str(
                item.get("candidate_answer", "")
            ).strip(),
            relevant=bool(item.get("relevant", False)),
        )
        for item in data.get("items", [])
    ]
