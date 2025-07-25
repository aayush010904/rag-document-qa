import requests
import time

url = "http://localhost:8000/hackrx/run"
headers = {
    "Authorization": "Bearer b689cc51239dbe57b19d7432235ab5fd0adc0ab7bd705f4cb51920ec4c53ce9e",
    "Content-Type": "application/json"
}

questions= [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]

payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": questions
}

start_time = time.time()
response = requests.post(url, headers=headers, json=payload)
end_time = time.time()

total_time = end_time - start_time

if response.status_code == 200:
    answers = response.json().get("answers", [])
    print("✅ Response:\n")
    # for i, (q, a) in enumerate(zip(questions, answers), start=1):
    #     print(f"Q{i}: {q}")
    #     print(f"A{i}: {a}\n")
    for i in answers:
        print(f"A -  {i}\n\n")
    print(f"Total Latency for {len(questions)} questions: {total_time:.2f} seconds")
    print(f"Average Latency per question: {total_time / len(questions):.2f} seconds")
else:
    print(f"❌ Error {response.status_code}:")
    print(response.text)
