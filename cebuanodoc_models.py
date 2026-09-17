import subprocess
import re


GEMMA_MODEL = "gemma4:e2b"
MEDGEMMA_MODEL = "medgemma:latest"


def run_model(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


def clean_output(text):
    ansi_pattern = re.compile(
        r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
    )
    text = ansi_pattern.sub('', text)

    marker = "...done thinking."
    if marker in text:
        text = text.split(marker, 1)[1]

    text = text.replace("**", "")
    text = text.replace("###", "")
    text = text.replace("##", "")

    return text.strip()


def translate_to_english(text):
    prompt = f"""
TASK: Translate the following Cebuano text to English.

Do not answer the question.
Do not explain anything.
Preserve all medical information.
Output only the English translation.

TEXT:
{text}
"""

    response = run_model(GEMMA_MODEL, prompt)

    return clean_output(response)


def get_medical_response(text):
    prompt = f"""
A patient says:

"{text}"

Respond to the patient with helpful general medical guidance.

You MUST answer the patient's concern instead of repeating,
rewriting, or translating their statement.

Provide:
- useful general advice
- possible common explanations when appropriate
- warning signs to watch for
- when professional medical care may be needed

Do not make a definite diagnosis.

Answer directly in English.

MEDICAL RESPONSE:
"""

    response = run_model(MEDGEMMA_MODEL, prompt)

    return clean_output(response)


def translate_to_cebuano(text):
    prompt = f"""
TASK: Translate the medical response below into natural Cebuano.

Do not answer it again.
Do not add new medical information.
Do not remove warnings or safety information.
Preserve medication names, numbers, dosages, and durations.
Output only the Cebuano translation.

MEDICAL RESPONSE:
{text}

CEBUANO TRANSLATION:
"""

    response = run_model(GEMMA_MODEL, prompt)

    return clean_output(response)