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

    # 0. Taal: browsertaal bepaalt de startaal, Engels als standaard
    for loc, want in [("nl-NL", "nl"), ("es-ES", "es"), ("de-DE", "en")]:
        ctx = b.new_context(locale=loc, viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        pg.add_init_script("try{localStorage.setItem('dk-welcome','1');localStorage.setItem('dk-start','1')}catch(e){}")
        pg.goto(URL); pg.wait_for_timeout(300)
        got = pg.evaluate("lang")
        check(f"0 browsertaal {loc} geeft taal {want}", got == want, got)
        ctx.close()

    # 1d. Actief profiel: markering in de profielenlijst, "gewijzigd" na een wijziging, opnieuw actief na laden
    pg, errs = new_page(b)
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; recalc(); }")
    pg.evaluate("() => document.getElementById('scenDlg').showModal()"); pg.wait_for_timeout(200)
    pg.fill("#scenName", "Basis"); pg.click("#scenSave"); pg.wait_for_timeout(200)
    pg.fill("#scenName", "Hoog"); pg.evaluate("() => { manualAmount = 500000; amountNow = 500000; recalc(); }")
    pg.click("#scenSave"); pg.wait_for_timeout(200)
    check("1d na opslaan is het laatste profiel actief", pg.locator(".scenrow.active", has_text="Hoog").count() == 1)
    pg.locator(".scenrow", has_text="Basis").locator("[data-load]").click(); pg.wait_for_timeout(300)
    pg.evaluate("() => { renderScenarios(); document.getElementById('scenDlg').showModal(); }"); pg.wait_for_timeout(200)
    check("1e na laden is Basis actief", pg.locator(".scenrow.active", has_text="Basis").count() == 1)
    check("1e' zonder wijziging geen 'gewijzigd'", "gewijzigd" not in pg.inner_text("#scenList") and "changed" not in pg.inner_text("#scenList"))
    pg.evaluate("() => document.getElementById('scenDlg').close()")
    pg.evaluate("() => { manualAmount = 400000; amountNow = 400000; recalc(); }")
    pg.evaluate("() => { renderScenarios(); document.getElementById('scenDlg').showModal(); }"); pg.wait_for_timeout(200)
    check("1f na wijzigen staat 'gewijzigd' bij het actieve profiel", pg.locator(".scenrow.active", has_text="Basis").count() == 1 and ("gewijzigd" in pg.inner_text("#scenList") or "changed" in pg.inner_text("#scenList")))
    pg.close()

    # 1h. Profiel laden bij niet-opgeslagen wijzigingen vraagt eerst: opslaan of niet opslaan
    pg, errs = new_page(b)
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; recalc(); }")
    pg.evaluate("() => document.getElementById('scenDlg').showModal()"); pg.wait_for_timeout(200)
    pg.fill("#scenName", "Basis"); pg.click("#scenSave"); pg.wait_for_timeout(200)
    pg.fill("#scenName", "Hoog"); pg.evaluate("() => { manualAmount = 500000; amountNow = 500000; recalc(); }")
    pg.click("#scenSave"); pg.wait_for_timeout(200)
    pg.evaluate("() => { manualAmount = 400000; amountNow = 400000; recalc(); }")
    pg.click('[data-load="0"]'); pg.wait_for_timeout(300)
    check("1h bij wijzigingen verschijnt de vraag en blijft de dialoog open", pg.is_visible("#scenPrompt") and pg.evaluate("document.getElementById('scenDlg').open"))
    pg.click("#scenPCancel"); pg.wait_for_timeout(200)
    check("1i annuleren laadt niets", pg.evaluate("amountNow") == 400000)
    pg.click('[data-load="0"]'); pg.wait_for_timeout(300)
    pg.click("#scenPDiscard"); pg.wait_for_timeout(300)
    check("1j niet opslaan laadt het gekozen profiel", pg.evaluate("amountNow") == 330000)
    check("1k niet opslaan wijzigt het andere profiel niet", pg.evaluate("loadScen().find(x=>x.name==='Hoog').data.amount") == 500000)
    pg.close()

    # 10. Spaarrente telt mee: spaardeel groeit met de rente en staat in netto waarde en tabel
    pg, errs = new_page(b)
    pg.evaluate("() => { manualAmount = 100000; amountNow = 100000; pickResid('nl'); recalc(); }")
    pg.evaluate("() => { const s=document.getElementById('savePct'); s.value=50; s.dispatchEvent(new Event('input')); const r=document.getElementById('savRate'); r.value='4'; r.dispatchEvent(new Event('input')); }")
    pg.wait_for_timeout(300)
    got = pg.evaluate("savAt(10)")
    check("10a spaarbedrag groeit met samengestelde rente", abs(got - 50000 * 1.04 ** 10) < 0.01, got)
    pg.evaluate("document.querySelector('.tabs .tab[data-tab=\"tabWealth\"]').click()"); pg.wait_for_timeout(300)
    txt = pg.inner_text("#wealthBody")
    import re
    check("10b netto waarde toont spaargeld na 10 jaar", re.search(r"74[.,]012", txt) is not None)
    pg.evaluate("() => { const r=document.getElementById('savRate'); r.value='0'; r.dispatchEvent(new Event('input')); }"); pg.wait_for_timeout(300)
    check("10c bij 0% rente blijft het spaardeel gelijk", abs(pg.evaluate("savAt(10)") - 50000) < 0.01)
    check("10d geen fouten", not errs, errs)
    pg.close()

    # 11. Export: vier keuzes met uitleg, story-kaart en adviesoverzicht
    pg, errs = new_page(b)
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; monthlyAmt = 250; pickResid('nl'); taxOn.us = true; taxOn.nl = true; updateChips(); recalc(); }")
    pg.evaluate("() => { renderExpDlg(); document.getElementById('expDlg').showModal(); }"); pg.wait_for_timeout(200)
    check("11a exportdialoog toont vier keuzes", pg.locator("#expOpts .expopt").count() == 4)
    pg.hover('[data-exp="story"]'); pg.wait_for_timeout(150)
    check("11b voorbeeld verschijnt bij hover", "Instagram" in pg.inner_text("#expPreview") or "kaart" in pg.inner_text("#expPreview").lower() or "card" in pg.inner_text("#expPreview").lower())
    size = pg.evaluate("() => { const c = buildStoryCanvas(); return [c.width, c.height]; }")
    check("11c story-kaart is 1080x1920", size == [1080, 1920], size)
    html = pg.evaluate("() => buildReport()")
    check("11d adviesoverzicht bevat alle onderdelen", all(x in html for x in ["Uitgangspunten", "Fondsen", "Resultaat", "Netto vermogen per jaar", "Belasting per land", "voorbehoud"]) or all(x in html for x in ["Starting points", "Funds", "Result", "Net worth per year", "Tax per country", "disclaimer"]))
    pg.evaluate("document.getElementById('expDlg').close()")
    check("11e geen fouten", not errs, errs)
    pg.close()

    # 1. Roundtrip: alle opgeslagen waarden komen terug
    pg, errs = new_page(b)
    set_domicile(pg, "nl")
    pg.evaluate("() => { manualAmount = 330000; amountNow = 330000; monthlyAmt = 250; recalc(); }")
    pg.evaluate("() => { taxOn.us = true; taxOn.ar = true; updateChips(); }")
    pg.evaluate("() => { const s = document.getElementById('savePct'); s.value = 7.25; s.dispatchEvent(new Event('input')); }")
    pg.evaluate("document.querySelector('.tabs .tab[data-tab=\"tabTax\"]').click()"); pg.wait_for_timeout(300)
    pg.fill("#savRate", "3,5")
    pg.wait_for_timeout(100)
    before = pg.evaluate("captureState()")
    pg.evaluate("() => { savePct = 0; document.getElementById('savePct').value = 0; document.getElementById('savRate').value = '1'; }")
    pg.evaluate("s => applyState(s)", before)
    pg.wait_for_timeout(200)
    after = pg.evaluate("captureState()")
    check("1 profiel opslaan en laden: waarden gelijk", before == after, f"{before} vs {after}")
    check("1a spaarrente opgeslagen en teruggezet", pg.input_value("#savRate") == "3,5", pg.input_value("#savRate"))
    check("1c voorbeeld spaarrente toont bedrag", "€" in pg.inner_text("#savInt"), pg.inner_text("#savInt"))
    check("1b geen fouten bij laden", not errs, errs)
    pg.close()

    # 2. Domicilie blijft na herladen en na reset
    pg, errs = new_page(b)
    set_domicile(pg, "ve")
    pg.reload(); pg.wait_for_timeout(900)
    check("2a domicilie na herladen", pg.eval_on_selector("#resid", "e => e.value") == "ve")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(1500)
    check("2b domicilie na reset gewist", pg.eval_on_selector("#resid", "e => e.value") == "")
    pg.close()

    # 3. Landen blijven na reset
    pg, errs = new_page(b)
    set_domicile(pg, "ve")
    pg.evaluate("() => { taxOn.us = true; taxOn.fr = true; saveLast(); }")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(1500)
    picked = pg.evaluate("Object.keys(taxOn).filter(k => taxOn[k]).sort().join(',')")
    check("3 landen na reset gewist", picked == "", picked)
    pg.close()

    # 4. Profielen blijven na reset
    pg, errs = new_page(b)
    pg.evaluate("() => localStorage.setItem('dk-scenarios', JSON.stringify([{name:'Test',date:'15-10-2026',ts:Date.now(),data:{}}]))")
    pg.evaluate("document.getElementById('menuReset').click()"); pg.wait_for_timeout(1200)
    kept = pg.evaluate("localStorage.getItem('dk-scenarios')")
    check("4 profielen na reset behouden", kept is not None and "Test" in kept, kept)
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
