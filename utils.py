# import os
# import tempfile
# import requests
# import asyncio
# import aiohttp
# from typing import List
# from openai import OpenAI
# from sentence_transformers import SentenceTransformer
# import faiss
# import fitz  # PyMuPDF
# from dotenv import load_dotenv

# # Load environment
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Groq LLM client
# groq_client = OpenAI(
#     api_key=GROQ_API_KEY,
#     base_url="https://api.groq.com/openai/v1"
# )

# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     full_text = []

#     for page in doc:
#         text = page.get_text("text")
#         if not text.strip():
#             # fallback to raw blocks if empty
#             text = page.get_text("blocks")
#         full_text.append(text if isinstance(text, str) else "\n".join([str(b) for b in text]))

#     return "\n".join(full_text)


# def chunk_text(text: str, chunk_size=500, overlap=50):
#     lines = text.split('\n')
#     chunks = []
#     chunk = ''

#     for line in lines:
#         if len(chunk) + len(line) < chunk_size:
#             chunk += line.strip() + ' '
#         else:
#             chunks.append(chunk.strip())
#             chunk = line.strip() + ' '
    
#     if chunk:
#         chunks.append(chunk.strip())

#     return chunks



# def embed_chunks(chunks: List[str]):
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     embeddings = model.encode(chunks)
#     index = faiss.IndexFlatL2(384)
#     index.add(embeddings.astype("float32"))
#     return index, chunks, model


# async def ask_question(question: str, index, docs, model) -> str:
#     try:
#         # Embed and retrieve top-3 chunks
#         q_embedding = model.encode([question])
#         _, top_idxs = index.search(q_embedding, 3)
#         top_chunks = "\n".join([docs[i] for i in top_idxs[0]])

#         # Tight, latency-optimized prompt
#         prompt = f"""
# You are a professional assistant for insurance policy queries.  
# Answer the user's question using only the clauses provided.

# CLAUSES:
# {top_chunks}

# QUESTION:
# {question}

# GUIDELINES:
# - Answer only if the information is explicitly present.
# - Include specific coverage terms like waiting periods, monetary limits, percentage caps, plan names, or durations — if mentioned.
# - If the clause references a law or act (e.g., “XYZ Act, 1994”), mention its name exactly as stated — but do not explain it or add legal terms.
# - If a clause refers to a table, extract and clearly include the value (e.g., “1% of Sum Insured”, “INR 5,000”, “24 months”).
# - If both inclusion and exclusion clauses are present, prioritize clauses that clearly mention coverage and conditions, and mention exclusions only if they override that specific coverage.
# - Avoid legal tone. Write in natural, simple English.
# - Do not say things like “as per policy”, “according to clause”, or “section 3.4”.
# - If the answer is not found, respond exactly: "Not mentioned in the policy."
# - Limit the response to 35 words or less.
# """





#         # Call Groq LLM (streaming optional)
#         response = groq_client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.0,
#             max_tokens=80,
#         )

#         return response.choices[0].message.content.strip()

#     except Exception as e:
#         return f"Error: {str(e)}"


# async def process_document_and_answer(blob_url: str, questions: list[str]) -> list[str]:
#     # Step 1: Download PDF
#     response = requests.get(blob_url)
#     if response.status_code != 200:
#         raise Exception("Failed to download PDF from blob URL.")

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(response.content)
#         tmp_path = tmp.name

#     # Step 2: Extract text, chunk, embed
#     text = extract_text_from_pdf(tmp_path)
#     chunks = chunk_text(text)
#     index, docs, model = embed_chunks(chunks)
#     os.remove(tmp_path)

#     # Step 3: Parallel question answering
#     tasks = [ask_question(q, index, docs, model) for q in questions]
#     answers = await asyncio.gather(*tasks)
#     return answers


import os
import tempfile
import requests
import asyncio
from typing import List
import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Init clients
groq_client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    full_text = []
    for page in doc:
        text = page.get_text("text")
        if not text.strip():
            text = page.get_text("blocks")
        full_text.append(text if isinstance(text, str) else "\n".join([str(b) for b in text]))
    return "\n".join(full_text)


def chunk_text(text: str, chunk_size=500, overlap=50):
    lines = text.split('\n')
    chunks = []
    chunk = ''
    for line in lines:
        if len(chunk) + len(line) < chunk_size:
            chunk += line.strip() + ' '
        else:
            chunks.append(chunk.strip())
            chunk = line.strip() + ' '
    if chunk:
        chunks.append(chunk.strip())
    return chunks


def embed_and_store_chunks(chunks: List[str]):
    embeddings = model.encode(chunks)
    vectors = [
        {"id": f"chunk-{i}", "values": emb.tolist(), "metadata": {"text": chunk}}
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]
    index.upsert(vectors=vectors)


def query_top_chunks(query: str, top_k=3) -> str:
    query_vec = model.encode([query])[0].tolist()
    res = index.query(vector=query_vec, top_k=top_k, include_metadata=True)
    return "\n".join([match["metadata"]["text"] for match in res["matches"]])


async def ask_question(question: str) -> str:
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


async def process_document_and_answer(blob_url: str, questions: list[str]) -> list[str]:
    response = requests.get(blob_url)
    if response.status_code != 200:
        raise Exception("Failed to download PDF from blob URL.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    chunks = chunk_text(text)
    embed_and_store_chunks(chunks)
    os.remove(tmp_path)
    tasks = [ask_question(q) for q in questions]
    return await asyncio.gather(*tasks)
