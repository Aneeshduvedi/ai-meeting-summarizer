
import json

from meetings.services.groq_client import get_groq_client


MODEL_NAME = "openai/gpt-oss-20b"


def analyze_meeting(transcript: str) -> dict:
    if not transcript or not transcript.strip():
        raise ValueError("Meeting transcript cannot be empty.")

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a meeting analysis agent.

Use ONLY the information in the supplied transcript.
Do not use outside knowledge or invent facts.

Return valid JSON with this exact structure:
{
  "summary": "A concise summary supported by the transcript",
  "topics": ["Topic explicitly discussed"]
}

Rules:
- Include only information supported by the transcript.
- Do not invent decisions, tasks, owners, or deadlines.
- If the transcript is unclear, state that in the summary.
- Return JSON only, without Markdown fences.
"""
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError(
            "The AI returned invalid JSON. Please try again."
        ) from exc

    if not isinstance(result, dict):
        raise ValueError("The AI response must be a JSON object.")

    if not isinstance(result.get("summary"), str):
        raise ValueError("The AI response is missing a valid summary.")

    if not isinstance(result.get("topics"), list):
        raise ValueError("The AI response is missing a valid topics list.")

    return result
