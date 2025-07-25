from openai import OpenAI
from config import GROQ_API_KEY
from vector_store import query_top_chunks

groq_client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


async def ask_question(question: str) -> str:
    """Ask question using LLM with retrieved context."""
    try:
        top_chunks = query_top_chunks(question, top_k=3)
        prompt = f"""
You are a precise insurance assistant.

Answer the question using only the following clauses:

{top_chunks}

QUESTION:
{question}

RESPONSE RULES:
- Answer in plain, clear English.
- Limit to 1–2 sentences and under 35 words.
- Include specific figures (e.g., “INR 5,000”, “1% of SI”, “24 months”) if mentioned.
- Do NOT say “Based on clauses”, “I found”, “Clause number”, or similar.
- DO NOT add friendly or formal tone (e.g., “I’m happy to help” or “Please let me know…”).
- If the policy mentions any legal act or law, write it **exactly** as written (e.g., “Transplantation of Human Organs Act, 1994”).
- If the answer is missing, say exactly: **"Not mentioned in the policy."**
"""
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=80,
        )

        answer = response.choices[0].message.content
        return answer.strip() if answer else "No response generated"
    except Exception as e:
        return f"Error: {str(e)}"
