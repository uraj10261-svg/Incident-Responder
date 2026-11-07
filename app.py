import os, pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import engine, memory, llm
from gen import TRUTH

CSV = "incidents.csv"
app = FastAPI()
load = lambda: pd.read_csv(CSV) if os.path.exists(CSV) else pd.DataFrame(columns=["service", "symptom", "root_cause", "fix", "resolved"])

class Alert(BaseModel):
    symptom: str
class Outcome(BaseModel):
    service: str; symptom: str; root_cause: str; fix: str; resolved: bool

@app.get("/")
def home(): return FileResponse("index.html")

@app.get("/symptoms")
def symptoms(): return list(TRUTH)

@app.post("/alert")
def alert(a: Alert):
    s = engine.suggest(load(), a.symptom); snips = memory.recall(a.symptom)
    return dict(stats=s, recalled=snips, explanation=llm.explain(s, snips))

@app.post("/outcome")
def outcome(o: Outcome):
    row = {**o.model_dump(), "resolved": int(o.resolved)}
    pd.concat([load(), pd.DataFrame([row])]).to_csv(CSV, index=False)
    return dict(saved=True, remembered=memory.retain(row), total=len(load()))
