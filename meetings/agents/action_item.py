
import json

from meetings.services.groq_client import get_groq_client


MODEL_NAME = "openai/gpt-oss-20b"


def extract_action_items(transcript: str) -> dict:
    if not transcript or not transcript.strip():
        raise ValueError("Meeting transcript cannot be empty.")

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a meeting action-item extraction agent.

Use ONLY information explicitly supported by the transcript.
Do not use outside knowledge or invent details.

Return valid JSON with exactly these keys:
{
  "decisions": [],
  "action_items": [
    {
      "task": "",
      "owner": "Not specified",
      "deadline": "Not specified"
    }
  ],
  "unresolved_questions": []
}

Rules:
- Include only decisions explicitly made in the transcript.
- Include only tasks explicitly agreed upon or assigned.
- Use "Not specified" when an owner or deadline is missing.
- Include unresolved questions only when the transcript supports them.
- If no items exist for a category, return an empty list.
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

    for key in ("decisions", "action_items", "unresolved_questions"):
        if not isinstance(result.get(key), list):
            raise ValueError(f"The AI response has an invalid '{key}' field.")

    for item in result["action_items"]:
        if not isinstance(item, dict) or not isinstance(item.get("task"), str):
            raise ValueError("The AI returned an invalid action item.")

        item.setdefault("owner", "Not specified")
        item.setdefault("deadline", "Not specified")

    return result
