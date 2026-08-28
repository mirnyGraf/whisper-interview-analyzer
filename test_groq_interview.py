import json

from whisper_ui.interview.groq_client import (
    create_groq_client_from_env,
)
from whisper_ui.interview.groq_interview_analyzer import (
    analyze_interview,
)
from whisper_ui.interview.roles import assign_roles
from whisper_ui.interview.turns import merge_segments_into_turns


with open("interview_test.json", "r", encoding="utf-8") as file:
    data = json.load(file)

segments = data["segments"]

turns = merge_segments_into_turns(segments)

# Комментарии: для этого тестового интервью роли уже известны.
role_turns = assign_roles(
    turns,
    interviewer_speaker="SPEAKER_01",
    candidate_speaker="SPEAKER_00",
)

client = create_groq_client_from_env()

try:
    result = analyze_interview(
        role_turns,
        client=client,
    )
finally:
    client.close()

print("=" * 80)
print(f"НАЙДЕНО ВОПРОСОВ: {len(result)}")
print("=" * 80)

for number, item in enumerate(result, start=1):
    print()
    print(f"{number}. ВОПРОС:")
    print(item.question)

    print()
    print("ОТВЕТ КАНДИДАТА:")
    print(item.candidate_answer or "[ответ не найден]")

    print()
    print(f"СОДЕРЖАТЕЛЬНЫЙ: {item.relevant}")

    print("-" * 80)
