import os, json
from dotenv import load_dotenv
load_dotenv()

def explain(s: dict, snippets: list[str]) -> str:
    """LLM explains the given numbers; falls back to a template on any error."""
    top = s["fixes"][0]
    fallback = f"Based on {s['n']} similar incidents ({s['confidence']} confidence), likely cause: {s['cause']}. Try '{top['fix']}' first."
    try:
        from groq import Groq
        r = Groq(api_key=os.environ["GROQ_API_KEY"]).chat.completions.create(
            model="openai/gpt-oss-120b", temperature=0.2,
            messages=[{"role": "system", "content": "You are an on-call assistant. Use ONLY the numbers given. Never invent numbers. 3 sentences max; say so if confidence is low or history is missing."},
                      {"role": "user", "content": json.dumps({"stats": s, "recalled": snippets})}])
        return r.choices[0].message.content
    except Exception:
        return fallback
