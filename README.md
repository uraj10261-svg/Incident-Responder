# Incident Responder

When something breaks in production at 3 a.m., the on-call engineer usually spends the next half hour guessing, or digging through old tickets for a fix the team already found months ago. I built Incident Responder to fix that. You pick the alert that fired, and it tells you which fix has worked most often before, and why. Then you log whether it worked, and the next suggestion gets a little smarter.

**Heads up:** this is a prototype. It isn't finished and it isn't ready for real production use. I've listed what's missing below.

## Why bother

- You get one clear suggestion in seconds, so there's less guessing under pressure.
- What the team has learned stays with the team, even when people move on.
- It improves every time someone logs an outcome.
- It's honest about confidence. If it has little or no history for an alert, it says so.
- The numbers are worked out in plain code. The AI only explains them, so it can't make up statistics.

## How it works

1. Pick the alert that fired.
2. The app ranks the possible fixes by how often each one worked. Fixes with only a few tries are discounted, so one lucky result doesn't win.
3. Hindsight, the memory layer, recalls similar past incidents, and an AI model turns the numbers into a short explanation.
4. You log whether the fix worked, and it's saved for next time.

## What it's built with

- **Backend:** Python and FastAPI
- **Statistics:** pandas
- **Memory:** Hindsight
- **Explanations:** Groq (`openai/gpt-oss-120b`)
- **Data:** a CSV file, `incidents.csv`
- **Frontend:** a single HTML file with plain JavaScript and CSS

## Running it

```
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env           # Mac/Linux: cp .env.example .env
python gen.py                    # makes the sample incidents
python seed.py                   # optional: loads them into Hindsight
uvicorn app:app --reload
```

Put your `GROQ_API_KEY`, `HINDSIGHT_API_KEY` and `HINDSIGHT_BASE_URL` in `.env`, then open http://127.0.0.1:8000. It still runs without keys, but you'll get a basic template explanation and no recalled memory.

Run the tests with `pytest -q`, and the learning-curve demo with `python curve.py`.

## Does it actually learn?

On the sample data, yes. This is how often its top suggestion was the right fix:

| Incidents it has seen | Right suggestion |
|---|---|
| 0 | 20% |
| 10 | 93% |
| 25 | 93% |
| 50 | 100% |

Take these numbers with a grain of salt. The sample data is made up and has a very clear pattern built in. Real incidents are messier, so real results would improve more slowly.

## What's missing

- The data is synthetic, not from a real team.
- The rankings come from the CSV. Hindsight adds the recalled context, but it doesn't drive the numbers.
- Alerts are matched by type only, not by logs, metrics or wording.
- There's no login or access control, and the CSV is a stand-in for a real database.
- The AI explanation sometimes mixes up which number means what, so trust the figures on screen over the text.
- The live Hindsight and Groq calls have no automated tests.

## Where it could go next

- **An admin panel** so admins can add new problems, causes and fixes from the frontend, without touching code.
- **Company profiles**, where each company gets its own workspace and memory, plus admin accounts that control only their own data, users and alerts.
- A real database, with login and user roles.
- Matching on logs and metrics, and connecting to tools like PagerDuty or Datadog.
- Real timestamps on memories, so recent incidents count for more.
- More tests, including the live Hindsight and Groq calls.
