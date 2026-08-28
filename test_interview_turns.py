import json
from pathlib import Path

from whisper_ui.interview.roles import assign_roles
from whisper_ui.interview.turns import merge_segments_into_turns
from whisper_ui.interview.questions import extract_interviewer_questions
from whisper_ui.interview.qa_pairs import extract_qa_pairs

json_path = Path("interview_test.json")

with json_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

segments = data["segments"]

# Комментарии: сначала объединяем мелкие Whisper-сегменты в цельные реплики.
turns = merge_segments_into_turns(segments)

# Комментарии: для этого тестового интервью роли задаём вручную.
# Комментарии: SPEAKER_01 — интервьюер.
# Комментарии: SPEAKER_00 — кандидат.
role_turns = assign_roles(
    turns,
    interviewer_speaker="SPEAKER_01",
    candidate_speaker="SPEAKER_00",
)

print(f"Исходных сегментов: {len(segments)}")
print(f"Объединённых реплик: {len(turns)}")
print()

for number, turn in enumerate(role_turns[:20], start=1):
    print(
        f"{number}. [{turn.start:.1f}–{turn.end:.1f}] "
        f"{turn.role} ({turn.speaker})"
    )
    print(turn.text)
    print("-" * 80)
questions = extract_interviewer_questions(role_turns)

print()
print("=" * 80)
print(f"ВОПРОСОВ ИНТЕРВЬЮЕРА: {len(questions)}")
print("=" * 80)

for number, question in enumerate(questions, start=1):
    print(f"{number}. {question.text}")
qa_pairs = extract_qa_pairs(role_turns)

print()
print("=" * 80)
print(f"ПАР ВОПРОС -> ОТВЕТ: {len(qa_pairs)}")
print("=" * 80)

for number, pair in enumerate(qa_pairs, start=1):
    print(f"\n{number}. ВОПРОС:")
    print(pair.question)

    print("\nОТВЕТ КАНДИДАТА:")
    print(pair.answer or "[Ответ не найден]")

    print("-" * 80)
