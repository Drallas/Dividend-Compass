"""Testplan Dividend Compass. Zie TESTPLAN.md. Draai met: python3 tests/run_tests.py"""
import os, sys
from playwright.sync_api import sync_playwright

URL = "file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))
results = []

def check(name, ok, detail=""):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + (("  " + str(detail)) if detail and not ok else ""))

def new_page(b):
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    pg.add_init_script("try{localStorage.setItem('dk-welcome','1');localStorage.setItem('dk-start','1')}catch(e){}")
    pg.goto(URL)
    pg.wait_for_timeout(400)
    return pg, errs

def set_domicile(pg, v):
    pg.evaluate("v => { const r = document.getElementById('resid'); r.value = v; r.dispatchEvent(new Event('change')); }", v)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    # 1. Roundtrip: alle opgeslagen waarden komen terug
    pg, errs = new_page(b)
    set_domicile(pg, "nl")
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; monthlyAmt = 250; recalc(); }")
    pg.evaluate("() => { taxOn.us = true; taxOn.ar = true; updateChips(); }")
    pg.evaluate("() => { const s = document.getElementById('savePct'); s.value = 7.25; s.dispatchEvent(new Event('input')); }")
    before = pg.evaluate("captureState()")
    pg.evaluate("() => { savePct = 0; document.getElementById('savePct').value = 0; }")
    pg.evaluate("s => applyState(s)", before)
    pg.wait_for_timeout(200)
    after = pg.evaluate("captureState()")
    check("1 profiel opslaan en laden: waarden gelijk", before == after, f"{before} vs {after}")
    check("1b geen fouten bij laden", not errs, errs)
    pg.close()

    # 2. Domicilie blijft na herladen en na reset
    pg, errs = new_page(b)
    set_domicile(pg, "ve")
    pg.reload(); pg.wait_for_timeout(400)
    check("2a domicilie na herladen", pg.eval_on_selector("#resid", "e => e.value") == "ve")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(800)
    check("2b domicilie na reset gewist", pg.eval_on_selector("#resid", "e => e.value") == "")
    pg.close()

    # 3. Landen blijven na reset
    pg, errs = new_page(b)
    set_domicile(pg, "ve")
    pg.evaluate("() => { taxOn.us = true; taxOn.fr = true; saveLast(); }")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(800)
    picked = pg.evaluate("Object.keys(taxOn).filter(k => taxOn[k]).sort().join(',')")
    check("3 landen na reset gewist", picked == "", picked)
    pg.close()

    # 4. Profielen blijven na reset
    pg, errs = new_page(b)
    pg.evaluate("() => localStorage.setItem('dk-scenarios', JSON.stringify([{name:'Test',date:'15-10-2026',ts:Date.now(),data:{}}]))")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(800)
    kept = pg.evaluate("localStorage.getItem('dk-scenarios')")
    check("4 profielen na reset behouden", kept is not None and "Test" in kept)
    # 4b. Alle andere invoer is gewist
    st = pg.evaluate("() => { try { return JSON.parse(localStorage.getItem('dk-last-v2')) || {}; } catch (e) { return {}; } }")
    clean = st.get("resid", "") == "" and len(st.get("tax", [])) == 0 and st.get("amount", 0) == 0
    check("4b na reset staat alleen de standaardwaarde opgeslagen", clean, st)
    pg.close()

    # 5. Box 3 verborgen bij niet-Nederland
    pg, errs = new_page(b)
    set_domicile(pg, "ve")
    hidden = pg.evaluate("getComputedStyle(document.querySelector('.savebox')).display") == "none"
    set_domicile(pg, "nl")
    shown = pg.evaluate("getComputedStyle(document.querySelector('.savebox')).display") != "none"
    check("5 box 3 verborgen bij niet-NL en zichtbaar bij NL", hidden and shown)
    pg.close()

    # 6. Maximaal vier landen
    pg, errs = new_page(b)
    set_domicile(pg, "nl")
    pg.evaluate("() => { ['us','ar','ve','fr'].forEach(k => taxOn[k] = true); updateChips(); }")
    dis = pg.evaluate("document.querySelector('#ovChips input[data-k=\"be\"]').disabled")
    check("6 overige landen uitgeschakeld bij vier", dis is True)
    pg.close()

    # 7. Landenlijst alfabetisch
    pg, errs = new_page(b)
    names = pg.evaluate("""() => { updateChips(); return [...document.querySelectorAll('#taxPick .cpick-list [data-nm]')].map(e => e.textContent); }""")
    check("7 landenlijst alfabetisch", names == sorted(names, key=str.lower), names)
    pg.close()

    # 8. Getypt bedrag blijft exact na opslaan en laden
    pg, errs = new_page(b)
    set_domicile(pg, "nl")
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; recalc(); }")
    pg.evaluate("document.querySelector('.tabs .tab[data-tab=\"tabTax\"]').click()"); pg.wait_for_timeout(300)
    pg.fill("#savAmt", "23925")
    st = pg.evaluate("captureState()")
    pg.evaluate("() => { savePct = 0; document.getElementById('savePct').value = 0; updateSaveLbl(); }")
    pg.evaluate("s => applyState(s)", st); pg.wait_for_timeout(200)
    amt = pg.input_value("#savAmt")
    check("8 getypt bedrag exact na laden", amt.replace(".", "").replace(",", "") == "23925", amt)
    pg.close()

    b.close()

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)} geslaagd, {len(failed)} gefaald")
sys.exit(1 if failed else 0)
