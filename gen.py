import random, pandas as pd
TRUTH = {  # symptom -> (root_cause, best_fix)
 "db_connections_high": ("connection pool leak", "restart worker"),
 "disk_full": ("unrotated logs", "rotate logs"),
 "error_rate_after_deploy": ("bad deploy", "rollback"),
 "memory_climbing": ("cache without eviction", "restart service"),
 "api_timeouts": ("upstream rate limit", "enable backoff"),
 "cpu_saturated": ("traffic spike", "scale out"),
}
FIXES = sorted({f for _, f in TRUTH.values()})
SERVICES = ["api", "payments", "search", "auth"]

def make(n=80, seed=42):
    """Generate n incidents; best fix resolves 85% of the time, others 15%."""
    r = random.Random(seed); rows = []
    for _ in range(n):
        s = r.choice(list(TRUTH)); cause, best = TRUTH[s]
        fix = best if r.random() < .5 else r.choice(FIXES)
        ok = r.random() < (.85 if fix == best else .15)
        rows.append(dict(service=r.choice(SERVICES), symptom=s, root_cause=cause, fix=fix, resolved=int(ok)))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    make().to_csv("incidents.csv", index=False)
