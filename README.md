# Web Quality Review

Skill **ตรวจคุณภาพงานเว็บที่สร้างด้วย AI ก่อนส่งมอบ** — แบ่งคะแนนเป็น 🧠 UX · 🎨 UI · ⚙️ Technical
และแยกเกณฑ์ตาม Track (Product / Project) × ประเภทเว็บ (Information / E-Commerce / Web Application)

**34–35 ข้อตรวจต่อรอบ** · คะแนน 100 · รายงาน HTML แบบ PageSpeed Insights

> ย้ายมาทำต่อใน Claude Code? อ่าน **[HANDOFF.md](HANDOFF.md)** ก่อน

---

## ติดตั้ง

**Claude Code** (แนะนำ — ตรวจได้เกือบ 100 คะแนน)
```bash
cd path/to/your-project && mkdir -p .claude/skills
git clone https://github.com/Krittiya-Amm/web-quality-review.git .claude/skills/web-quality-review
pip install playwright && playwright install chromium
```
commit ลง git ของโปรเจกต์ → ทั้งทีมได้ไปด้วย

**claude.ai** — Customize > Skills > "+" > Upload a skill (ZIP ที่มีโฟลเดอร์ `web-quality-review/` เป็นราก)
ข้อจำกัด: ออกเน็ตไปเว็บภายนอกไม่ได้ จึงตรวจกลุ่ม UI ไม่ได้

---

## ใช้งาน

```
/web-quality-review
```
หรือ `ตรวจเว็บนี้ก่อนส่งลูกค้า https://...`

Claude จะถาม **Track** และ **ประเภทเว็บ** ก่อน แล้วเช็ค readiness (IA / User Flow / Design Spec) ก่อนเริ่มตรวจ

**ตรวจ UI ให้ได้คะแนนจริง:**
```bash
python .claude/skills/web-quality-review/scripts/run-ui-probe.py https://example.com --out ./qa-output
```
ได้ `summary.md` + `probe-*.json` + `shot-*.png` 4 ขนาด แล้วบอก Claude ให้อ่านต่อ

---

## 3 กลุ่มคะแนน

| กลุ่ม | หมวด | 🅐 | 🅑 | 🅒 |
|---|---|---|---|---|
| 🧠 UX | UX1 Requirement & Content · UX2 IA & Navigation · UX3 Flow States & Interaction · UX4 ชุดเฉพาะประเภทเว็บ | 47 | 56 | 61 |
| 🎨 UI | UI1 Design System & Visual · UI2 Responsive Layout · UI3 Typography Contrast & Media | 38 | 33 | 31 |
| ⚙️ Tech | T1 Functional, Perf & SEO | 15 | 11 | 8 |

**สกิลนี้ตรวจผ่าน URL อย่างเดียว (link-only)** — Track ไม่ใช่หมวดคะแนนแล้ว แต่ใช้กำหนดความเข้มของคำตัดสินและเนื้อหาแท็บ "ความพร้อม & รอบถัดไป" · เรื่องที่ต้องเปิด repo ถึงตรวจได้ (DS version, regression, CI/CD, Handoff Section F, สิทธิ์ asset) อยู่นอกขอบเขตการให้คะแนน

**บังคับแสดง coverage** — แสดงที่ระดับกลุ่ม ว่าตรวจได้กี่ข้อจากกี่ข้อ · ถ้ารัน probe ไม่ได้ กลุ่ม UI เป็น Not Tested ทั้งกลุ่ม ห้ามให้คะแนน

| คะแนนรวม | 🟦 Product | 🟨 Project |
|---|---|---|
| มี Blocker ≥ 1 | 🚫 ห้าม merge/ship | 🚫 ห้ามส่งลูกค้า |
| 90–100 | ✅ พร้อม ship | ✅ พร้อมส่ง UAT |
| 80–89 | ⚠️ ควรแก้ Medium | ⚠️ ควรแก้ Medium |
| 70–79 | 🔧 ต้องแก้ก่อน merge | 🔧 ต้องแก้ก่อนรอบสุดท้าย |
| < 70 | 🚫 ยังไม่ควร ship | 🚫 ยังไม่ควรส่งมอบ |

---

## ใช้ที่ไหนได้คะแนนแค่ไหน

| สภาพแวดล้อม | UX | UI |
|---|---|---|
| **Claude Code** (รัน probe ได้) | ครบ | **ครบ** — วัดจริง 4 breakpoint |
| claude.ai (ออกเน็ตไปเว็บนอกไม่ได้) | เนื้อหา + IA เท่าที่ผู้ใช้ส่งให้ | ⚪ Not Tested ทั้งกลุ่ม |
| มีแต่ screenshot | — | เท่าที่ตาเห็น ไม่ใช่ค่าที่วัดได้ |

---

## คำศัพท์

**ติดตั้ง** (ครั้งเดียว) · **เรียกใช้** (ทุกครั้งที่ตรวจ) · **อัปเดต** (`git pull`) · **แชร์** (ส่งรีโปให้คนอื่นติดตั้ง)
