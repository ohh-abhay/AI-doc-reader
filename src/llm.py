
from openai import OpenAI

SYSTEM_PROMPT = """You are DocuMind, a document-grounded AI assistant.

Rules:
1. Answer using only the supplied document context.
2. If the context does not contain enough information, say you cannot find the answer in the provided documents.
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

    def generate(self, question: str, context: str, history=None) -> str:
        history_text = ""
        if history:
            recent = history[-6:]
            history_text = "\n".join(
                f"{m['role'].upper()}: {m['content']}"
                for m in recent
            )

        user_input = f"""Conversation history:
{history_text or "(none)"}

Document context:
{context}

User question:
{question}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                temperature=self.temperature,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Gemini request failed: {type(exc).__name__}: {exc}"
            ) from exc

        answer = response.choices[0].message.content
        return (answer or "I could not generate an answer.").strip()
