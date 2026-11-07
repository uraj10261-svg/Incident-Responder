import pandas as pd
GENERIC = "restart service"

def suggest(hist: pd.DataFrame, symptom: str) -> dict:
    """Rank fixes for a symptom by shrunk success rate from past incidents."""
    m = hist[hist.symptom == symptom]
    if m.empty:
        return dict(n=0, confidence="none", cause="unknown", fixes=[dict(fix=GENERIC, rate=0.0, tries=0)])
    g = m.groupby("fix").resolved.agg(ok="sum", tries="count")
    g["rate"] = (g.ok / (g.tries + 2)).round(2)  # shrinkage: few tries aren't over-trusted
    g = g.sort_values("rate", ascending=False).reset_index()
    cause = m[m.resolved == 1].root_cause.mode()
    return dict(n=len(m), confidence="low" if len(m) < 4 else "medium" if len(m) < 8 else "high",
                cause=cause.iat[0] if len(cause) else "unknown", fixes=g.to_dict("records"))
