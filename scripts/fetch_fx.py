"""Schrijft data/fx.json met de EUR->USD koers.

Bron koers: ECB-referentiekoers (officiële dagelijkse XML, geen sleutel nodig).
Bron gemiddelde (optioneel): Frankfurter, het 12-maands gemiddelde. Faalt dat, dan blijft avg12m leeg
en wordt de job niet afgebroken.
Faalt de ECB-koers, dan stopt het script met een foutmelding en blijft het oude bestand staan.
"""
import datetime
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ECB_DAILY = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
FRANKFURTER = "https://api.frankfurter.dev/v1"
OUT = "data/fx.json"
BRON = "ECB-referentiekoersen (ECB-XML); 12m-gemiddelde via Frankfurter. Wordt dagelijks bijgewerkt door GitHub Actions"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dividend-compass-fx/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} bij {url}: {e.read(300)!r}")


# 1. Dagkoers (verplicht)
root = ET.fromstring(get(ECB_DAILY))
ns = {"e": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
cube = root.find(".//e:Cube[@time]", ns)
if cube is None:
    sys.exit("ECB-XML: geen datum gevonden")
date = cube.attrib["time"]
usd = None
for c in cube.findall("e:Cube", ns):
    if c.attrib["currency"] == "USD":
        usd = float(c.attrib["rate"])
if usd is None:
    sys.exit("ECB-XML: geen USD-koers gevonden")
print("ECB", date, "USD", usd)

# 2. Gemiddelde van 12 maanden (optioneel)
avg = None
try:
    today = datetime.date.today()
    start = today - datetime.timedelta(days=365)
    series = json.loads(get(f"{FRANKFURTER}/{start.isoformat()}..{today.isoformat()}?base=EUR&symbols=USD"))
    vals = [d["USD"] for d in series["rates"].values() if "USD" in d]
    avg = round(sum(vals) / len(vals), 4) if vals else None
except Exception as e:
    print("Waarschuwing: 12m-gemiddelde niet opgehaald:", e)

out = {
    "updated": date,
    "base": "EUR",
    "rates": {"USD": usd},
    "avg12m": {"USD": avg},
    "bron": BRON,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok", out)
