import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def interpret_transaction(text):
    prompt = f"""Extract the transaction details from this sentence:
    '{text}'
    Return JSON with: date, amount, category, description, tax (if any).
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return {"parsed_result": response.choices[0].message['content']}
