import json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gen import make, TRUTH
from engine import suggest

def accuracy(d, n: int) -> float:
    """Share of test incidents where the top suggestion equals the planted best fix."""
    hist, test = d.iloc[:n], d.iloc[-30:]
    return sum(suggest(hist, s)["fixes"][0]["fix"] == TRUTH[s][1] for s in test.symptom) / len(test)

if __name__ == "__main__":
    d = make(120); stages = [0, 10, 25, 50, 90]; acc = [accuracy(d, n) for n in stages]
    for n, a in zip(stages, acc): print(f"retained={n:<3} correct={a:.0%}")
    json.dump(dict(zip(map(str, stages), acc)), open("learning_curve.json", "w"))
    plt.plot(stages, acc, marker="o"); plt.xlabel("retained incidents"); plt.ylabel("correct suggestion rate"); plt.savefig("learning_curve.png")
