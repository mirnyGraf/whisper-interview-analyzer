"""Shared message constants used across pipeline, worker, and export layers."""

# ruff: noqa: RUF001
from __future__ import annotations

# -- Download progress messages --
DOWNLOAD_EXTRACTING_INFO = "Получение информации о видео..."
DOWNLOAD_IN_PROGRESS = "Скачивание аудио..."
DOWNLOAD_GDRIVE_IN_PROGRESS = "Скачивание файла из Google Drive..."
DOWNLOAD_DONE = "Скачивание аудио завершено."
DOWNLOAD_TWITTER_RESTRICTED = "Не удалось скачать содержимое. Возможно, требуется авторизация или доступ ограничен."
DOWNLOAD_SOURCE_TRANSIENT = "Источник временно недоступен. Попробуйте позже."

# -- Pipeline progress messages --
PREPROCESS_CONVERTING = "Преобразование аудио в моно WAV 16 кГц..."
PREPROCESS_DONE = "Предобработка аудио завершена."

TRANSCRIBE_LOADING = "Загрузка модели распознавания..."
TRANSCRIBE_RUNNING = "Транскрибация аудио..."
TRANSCRIBE_DONE = "Транскрибация завершена."

ALIGN_LOADING = "Загрузка модели выравнивания..."
ALIGN_RUNNING = "Выравнивание временных меток..."
ALIGN_DONE = "Выравнивание завершено."
ALIGN_SKIPPED = "Выравнивание не удалось. Используются исходные временные метки."

DIARIZE_LOADING = "Загрузка модели разделения спикеров..."
DIARIZE_RUNNING = "Разделение спикеров..."
DIARIZE_RUNNING_HEARTBEAT = "Разделение спикеров... Выполняется {elapsed} сек."
DIARIZE_DONE = "Разделение спикеров завершено."
DIARIZE_SKIPPED = "Разделение спикеров пропущено: не указан HF Token."
DIARIZE_SKIPPED_DISABLED = "Разделение спикеров отключено пользователем."

ASSIGN_RUNNING = "Назначение спикеров сегментам..."
ASSIGN_DONE = "Назначение спикеров завершено."
ASSIGN_SKIPPED = "Назначение спикеров пропущено."
ASSIGN_FAILED = "Не удалось назначить спикеров. Используются сегменты без разметки."

POSTPROCESS_RUNNING = "Постобработка результата..."
POSTPROCESS_DONE = "Постобработка завершена."
POSTPROCESS_EMPTY = "Нет данных для постобработки."

LLM_CORRECTION_RUNNING = "LLM-коррекция текста ({done}/{total})..."
LLM_CORRECTION_DONE = "LLM-коррекция текста завершена."
LLM_CORRECTION_SKIPPED = "LLM-коррекция текста пропущена."
LLM_CORRECTION_DEGRADED = "LLM-коррекция частично завершилась с ошибкой. Исходный текст сохранён для сегментов:"

PIPELINE_COMPLETE = "Готово"
RESULT_PERSIST_FAILED = "Не удалось сохранить результат"

QUALITY_WARNING_REPETITIVE = "Обнаружена аномалия транскрипции: {percent}% сегментов повторяются (всего {total}). Возможная причина — тишина или музыка."

# -- Export --
EXPORT_DOCX_HEADING = "Результат транскрибации"
