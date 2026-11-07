import time, pandas as pd
import memory

rows = pd.read_csv("incidents.csv").to_dict("records")
ok = 0
for i, r in enumerate(rows, 1):
    ok += memory.retain(r)
    print(f"{i}/{len(rows)} retained={ok}", end="\r")
    time.sleep(0.3)
print(f"\nDone: {ok}/{len(rows)} stored in Hindsight")