from __future__ import annotations

from dataclasses import dataclass

from whisper_ui.interview.turns import DialogueTurn


@dataclass
class RoleTurn:
    role: str
    speaker: str
    start: float
    end: float
    text: str


def assign_roles(
    turns: list[DialogueTurn],
    interviewer_speaker: str,
    candidate_speaker: str,
) -> list[RoleTurn]:
    result: list[RoleTurn] = []

    for turn in turns:
        if turn.speaker == interviewer_speaker:
            role = "INTERVIEWER"
        elif turn.speaker == candidate_speaker:
            role = "CANDIDATE"
        else:
            role = "UNKNOWN"

        result.append(
            RoleTurn(
                role=role,
                speaker=turn.speaker,
                start=turn.start,
                end=turn.end,
                text=turn.text,
            )
        )

    return result
