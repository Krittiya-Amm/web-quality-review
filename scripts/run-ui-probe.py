#!/usr/bin/env python3
"""
run-ui-probe.py — รัน ui-probe.js กับเว็บเป้าหมายที่ 4 breakpoint พร้อม screenshot

ใช้กับ skill web-quality-review เพื่อเก็บหลักฐานกลุ่ม 🎨 UI

ติดตั้งครั้งเดียว:
    pip install playwright && playwright install chromium

ใช้งาน:
    python scripts/run-ui-probe.py https://example.com
    python scripts/run-ui-probe.py https://example.com --out ./qa-output
    python scripts/run-ui-probe.py ./index.html          # ไฟล์ในเครื่องก็ได้
    python scripts/run-ui-probe.py https://example.com --bp 390,834,1280

ผลลัพธ์ใน --out:
    probe-<w>.json   ค่าดิบทุก breakpoint
    shot-<w>.png     screenshot เต็มหน้า
    summary.md       ตารางสรุปให้ Claude อ่านต่อ
"""
import argparse, json, pathlib, sys

DEFAULT_BP = [375, 768, 1440, 1920]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="URL หรือ path ไฟล์ในเครื่อง")
    ap.add_argument("--out", default="./qa-output")
    ap.add_argument("--bp", default=",".join(map(str, DEFAULT_BP)),
                    help="ความกว้างที่จะตรวจ คั่นด้วย comma")
    ap.add_argument("--wait", type=int, default=900, help="ms รอหลังโหลด")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "ยังไม่ได้ติดตั้ง playwright — ติดตั้งก่อน:\n"
            "  macOS / Linux : pip3 install playwright && python3 -m playwright install chromium\n"
            "  Windows       : py -m pip install playwright && py -m playwright install chromium\n"
            "  Linux ถ้าเปิด browser ไม่ขึ้น : sudo python3 -m playwright install --with-deps chromium"
        )

    here = pathlib.Path(__file__).resolve().parent
    probe_path = here.parent / "assets" / "ui-probe.js"
    if not probe_path.exists():
        sys.exit(f"หา ui-probe.js ไม่เจอที่ {probe_path}")
    probe = probe_path.read_text(encoding="utf-8")

    target = args.target
    if not target.startswith(("http://", "https://")):
        p = pathlib.Path(target).resolve()
        if not p.exists():
            sys.exit(f"หาไฟล์ไม่เจอ: {p}")
        target = p.as_uri()

    outdir = pathlib.Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    bps = [int(x) for x in args.bp.split(",")]
    results, console_errors = {}, []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda m: console_errors.append(f"{m.type}: {m.text[:200]}")
                if m.type in ("error", "warning") else None)
        for w in bps:
            page.set_viewport_size({"width": w, "height": 900})
            try:
                page.goto(target, wait_until="networkidle", timeout=40000)
            except Exception as e:
                print(f"  ! {w}px โหลดไม่สำเร็จ: {type(e).__name__} — "
                      f"ถ้าเป็น 403 host_not_allowed แปลว่า network มี allowlist")
                continue
            page.wait_for_timeout(args.wait)
            data = page.evaluate(probe)
            results[w] = data
            (outdir / f"probe-{w}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            page.screenshot(path=str(outdir / f"shot-{w}.png"), full_page=True)
            u = data["tokens"]["uniqueCounts"]
            print(f"  {w:>5}px  h-scroll={str(data['horizontalScroll']):5} "
                  f"ล้นขอบ={len(data['overflowing']):<3} touch<44={data['smallTargetCount']:<3} "
                  f"contrast fail={data['contrastFailCount']:<3} "
                  f"สี={u['textColors']} ฟอนต์={u['fonts']} radius={u['radii']}")
        browser.close()

    if not results:
        sys.exit("ไม่ได้ผลลัพธ์เลย — ตรวจ network หรือ URL")

    write_summary(outdir, target, results, console_errors)
    print(f"\nเสร็จ → {outdir}/summary.md (ให้ Claude อ่านไฟล์นี้ต่อ)")

def write_summary(outdir, target, results, console_errors):
    widest = max(results)
    ref = results[widest]
    L = [f"# UI Probe Summary", "", f"- เป้าหมาย: `{target}`",
         f"- Breakpoint ที่ตรวจ: {', '.join(f'{w}px' for w in sorted(results))}", ""]

    L += ["## UI2 · Responsive", "",
          "| Breakpoint | h-scroll | element ล้นขอบ | touch < 44px |", "|---|---|---|---|"]
    for w in sorted(results):
        r = results[w]
        L.append(f"| {w}px | {'❌ มี' if r['horizontalScroll'] else '✅ ไม่มี'} "
                 f"| {len(r['overflowing'])} | {r['smallTargetCount']} |")

    # layout จัดใหม่จริงหรือย่อ desktop
    sizes_differ = len({json.dumps(results[w]['typography']['fontSizes'], sort_keys=True)
                        for w in results}) > 1
    L += ["", f"**Layout จัดใหม่จริงไหม:** "
          f"{'✅ font-size เปลี่ยนตาม breakpoint แปลว่ามี responsive rule จริง' if sizes_differ else '⚠️ font-size เท่ากันทุก breakpoint — อาจเป็นการย่อ desktop ลงมา ตรวจ screenshot ประกอบ'}", ""]

    u = ref["tokens"]["uniqueCounts"]
    L += ["## UI1 · Design System", "",
          f"| ค่าที่ใช้จริง | จำนวน | เกณฑ์คร่าวๆ |", "|---|---|---|",
          f"| สีข้อความ | {u['textColors']} | เกิน 8 = น่าจะไม่ได้มาจาก token |",
          f"| สีพื้นหลัง | {u['bgColors']} | เกิน 10 = น่าจะไม่ได้มาจาก token |",
          f"| ฟอนต์ | {u['fonts']} | เกิน 3 = มากเกินจำเป็น |",
          f"| border-radius | {u['radii']} | เกิน 4 = ไม่เป็นระบบ |",
          f"| box-shadow | {u['shadows']} | เกิน 4 = ไม่เป็นระบบ |",
          f"| ค่า spacing | {u['spacing']} | เกิน 12 = ไม่ได้ใช้ scale |", "",
          "สีข้อความที่ใช้ (เรียงตามความถี่) — เทียบกับ palette ของ DS หรือ CI ทีละค่า:", "",
          "```", json.dumps(ref["tokens"]["textColors"], ensure_ascii=False, indent=1)[:900], "```", ""]

    L += ["## UI3 · Typography, Contrast & Media", "",
          f"- ตัวอักษรต่ำกว่า 16px: `{list(ref['typography']['bodyBelow16'].keys()) or 'ไม่มี'}`",
          f"- contrast ไม่ผ่าน WCAG AA: **{ref['contrastFailCount']} จุด**",
          f"- H1 ในหน้า: {ref['headings']['counts']['h1']} · heading กระโดดลำดับ {ref['headings']['jumps']} ครั้ง",
          f"- รูปทั้งหมด {ref['media']['total']} · **แตก {len(ref['media']['broken'])}** "
          f"· ไม่มี alt {len(ref['media']['missingAlt'])} · ไม่กำหนด w/h {ref['media']['noDimensions']} "
          f"· ไม่ lazy {ref['media']['notLazy']}",
          f"- ฟอร์แมตรูป: `{ref['media']['formats']}`", ""]
    if ref["media"]["broken"]:
        L += ["**รูปที่แตกจริง:**", ""] + [f"- `{b}`" for b in ref["media"]["broken"][:10]] + [""]
    if ref["contrastFails"]:
        L += ["**contrast ที่ไม่ผ่าน (20 อันดับแรก):**", "",
              "| ratio | ต้องได้ | สีตัวอักษร | บนพื้น | ขนาด | ข้อความ |", "|---|---|---|---|---|---|"]
        for f in ref["contrastFails"][:20]:
            L.append(f"| {f['ratio']} | {f['need']} | `{f['fg']}` | `{f['bg']}` "
                     f"| {f['fontSize']} | {f['text'][:32]} |")
        L.append("")
    if ref["smallTargets"]:
        L += ["**touch target ที่เล็กกว่า 44px:**", ""]
        L += [f"- `{t['tag']}` {t['w']}×{t['h']}px — {t['label']}" for t in ref["smallTargets"][:15]] + [""]

    s = ref["seo"]
    L += ["## T1 · SEO & Meta", "", "| รายการ | ค่า |", "|---|---|",
          f"| title | {(s['title'] or '—')[:70]} |",
          f"| meta description | {'✅ มี' if s['description'] else '❌ ไม่มี'} |",
          f"| canonical | {s['canonical'] or '❌ ไม่มี'} |",
          f"| og:image | {s['ogImage'] or '❌ ไม่มี'} |",
          f"| og:title | {'✅ มี' if s['ogTitle'] else '❌ ไม่มี'} |",
          f"| twitter:card | {'✅ มี' if s['twitterCard'] else '❌ ไม่มี'} |",
          f"| favicon | {'✅ มี' if s['favicon'] else '❌ ไม่มี'} |",
          f"| JSON-LD structured data | {s['jsonLd'] if s['jsonLd'] else '❌ ไม่มี'} |",
          f"| html lang | {s['lang'] or '❌ ไม่ระบุ'} |", ""]

    if console_errors:
        uniq = list(dict.fromkeys(console_errors))[:15]
        L += ["## Console", ""] + [f"- `{e}`" for e in uniq] + [""]
    else:
        L += ["## Console", "", "ไม่พบ error หรือ warning", ""]

    L += ["---", "", "**ขั้นต่อไป:** ให้ Claude อ่านไฟล์นี้พร้อม `shot-*.png` "
          "แล้วนำไปให้คะแนนกลุ่ม UI ตาม `SKILL.md` ขั้นที่ 4 และ 7", ""]
    (outdir / "summary.md").write_text("\n".join(L), encoding="utf-8")

if __name__ == "__main__":
    main()
