"""Haalt de wisselkoers EUR->USD op (ECB-referentiekoers via Frankfurter) en schrijft data/fx.json.

Draait dagelijks via .github/workflows/fx.yml. Faalt de aanvraag, dan blijft het oude bestand staan.
"""
import datetime
import json
import urllib.request

BASE = "https://api.frankfurter.dev/v1"
CURRENCIES = ["USD"]
OUT = "data/fx.json"


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


today = datetime.date.today()
symbols = ",".join(CURRENCIES)

latest = get(f"{BASE}/latest?base=EUR&symbols={symbols}")
start = today - datetime.timedelta(days=365)
series = get(f"{BASE}/{start.isoformat()}..{today.isoformat()}?base=EUR&symbols={symbols}")

avg = {}
for c in CURRENCIES:
    vals = [day[c] for day in series["rates"].values() if c in day]
    avg[c] = round(sum(vals) / len(vals), 4) if vals else None

out = {
    "updated": latest["date"],
    "base": "EUR",
    "rates": {c: latest["rates"][c] for c in CURRENCIES},
    "avg12m": avg,
    "bron": "Frankfurter (ECB-referentiekoersen); wordt dagelijks bijgewerkt door GitHub Actions",
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok", out["updated"], out["rates"], out["avg12m"])
