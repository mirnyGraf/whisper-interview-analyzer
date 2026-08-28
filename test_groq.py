from whisper_ui.interview.groq_client import (
    create_groq_client_from_env,
)


client = create_groq_client_from_env()

try:
    result = client.chat(
        system="Ответь строго одним словом.",
        user="Напиши слово: работает",
    )

    print(result)
finally:
    client.close()

