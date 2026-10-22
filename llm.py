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
    def __init__(self, model: str, temperature: float = 0.2, api_key: str | None = None):
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = model
        self.temperature = temperature

    def generate(self, question: str, context: str, history=None) -> str:
        history_text = ""
        if history:
            recent = history[-6:]
            history_text = "\n".join(
                f"{m['role'].upper()}: {m['content']}" for m in recent
            )

        user_input = f"""Conversation history:
{history_text or "(none)"}

Document context:
{context}

User question:
{question}
"""
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=user_input,
        )
        return response.output_text.strip()
