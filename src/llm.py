import openai
from openai import OpenAI

SYSTEM_PROMPT = """You are DocuMind, a document-grounded AI assistant.

Rules:
1. Answer using ONLY the supplied document context.
2. If the context does not contain enough information, say you cannot find
   the answer in the provided documents.
3. Do not invent facts, page numbers, quotations, or sources.
4. Give a concise, professional answer.
5. When useful, refer to sources as [Source 1], [Source 2], etc.
"""


class LLMClient:
    def __init__(
        self,
        model: str,
        temperature: float = 0.2,
        api_key: str | None = None,
    ):
        if not api_key:
            raise ValueError("Please enter your Gemini API key.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self.model = model
        self.temperature = temperature

    def generate(try:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=self.temperature,
    )
except openai.APIStatusError as exc:
    details = str(exc)
    raise RuntimeError(
        f"Gemini API error (HTTP {exc.status_code}): {details[:800]}"
    ) from exc

answer = response.choices[0].message.content
return (answer or "I could not generate an answer.").strip()
            )

        user_input = f"""Conversation history:
{history_text or "(none)"}

Document context:
{context}

User question:
{question}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=self.temperature,
        )

        answer = response.choices[0].message.content
        return (answer or "I could not generate an answer.").strip()
