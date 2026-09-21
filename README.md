# Web Quality Review

Skill **ตรวจคุณภาพงานเว็บที่สร้างด้วย AI ก่อนส่งมอบ** — แบ่งคะแนนเป็น 🧠 UX · 🎨 UI · ⚙️ Technical
และแยกเกณฑ์ตาม Track (Product / Project) × ประเภทเว็บ (Information / E-Commerce / Web Application)

**34–35 ข้อตรวจต่อรอบ** · คะแนน 100 · รายงาน HTML แบบ PageSpeed Insights

> ย้ายมาทำต่อใน Claude Code? อ่าน **[HANDOFF.md](HANDOFF.md)** ก่อน

---

## ติดตั้ง

### Claude Code (แนะนำ — ตรวจได้ครบทั้ง 100 คะแนน)

ใช้ได้ทั้ง **macOS · Linux · Windows** — ตัวสกิลเป็น Python ล้วน ไม่ผูกกับ OS
ต้องมี **Python 3.8+** และ **git** ก่อน · คำสั่ง Python ต่างกันตาม OS ตามตารางนี้

| OS | คำสั่ง Python | คำสั่ง pip |
|---|---|---|
| macOS / Linux | `python3` | `pip3` |
| Windows | `py` | `py -m pip` |

**macOS / Linux**
```bash
cd path/to/your-project
mkdir -p .claude/skills
git clone https://github.com/Krittiya-Amm/web-quality-review.git .claude/skills/web-quality-review
pip3 install playwright && python3 -m playwright install chromium
```
Linux ถ้า browser เปิดไม่ขึ้น ให้ลง system library ด้วย:
`sudo python3 -m playwright install --with-deps chromium`

**Windows (PowerShell)**
```powershell
cd path\to\your-project
mkdir .claude\skills
git clone https://github.com/Krittiya-Amm/web-quality-review.git .claude/skills/web-quality-review
py -m pip install playwright
py -m playwright install chromium
```

playwright **จำเป็น** — ถ้าไม่มี กลุ่ม 🎨 UI จะเป็น Not Tested ทั้งกลุ่ม

**เช็คว่าติดตั้งสำเร็จ** (รันที่โฟลเดอร์โปรเจกต์)
```bash
# macOS / Linux
python3 .claude/skills/web-quality-review/scripts/run-ui-probe.py https://example.com --out ./probe-test
```
```powershell
# Windows
py .claude\skills\web-quality-review\scripts\run-ui-probe.py https://example.com --out .\probe-test
```
ได้ `summary.md` + `shot-*.png` 4 ไฟล์ = พร้อมใช้ (ลบโฟลเดอร์ `probe-test` ทิ้งได้)

commit โฟลเดอร์ `.claude/skills/` ลง git ของโปรเจกต์ → ทั้งทีมได้ไปด้วย

### claude.ai
Customize → Skills → **+** → Upload a skill (ZIP ที่มีโฟลเดอร์ `web-quality-review/` เป็นราก)
ข้อจำกัด: ออกเน็ตไปเว็บภายนอกไม่ได้ → ตรวจได้แค่ UX + Tech · กลุ่ม UI เป็น Not Tested

---

## วิธีใช้

### 1. เรียกสกิล

```
ตรวจเว็บนี้ก่อนส่งลูกค้า https://example.com
```
หรือพิมพ์ `/web-quality-review` · ประโยคอื่นที่เรียกติด: "ตรวจก่อน merge", "QA เว็บ", "รีวิวคุณภาพเว็บ", "เช็คความพร้อมก่อน handoff"

### 2. ตอบ 2 คำถาม

| คำถาม | ตัวเลือก | ไม่แน่ใจให้เลือก |
|---|---|---|
| **Track** | 🟦 Product (ของเราเอง iterate ต่อ) · 🟨 Project (งานลูกค้า one-off) | Product |
| **ประเภทเว็บ** | 🅐 Information · 🅑 E-Commerce · 🅒 Web Application | มีตะกร้า = 🅑 · มีล็อกอิน = 🅒 · อ่านเป็นหลัก = 🅐 |

ขนาดงาน Claude ประเมินเอง ไม่ต้องตอบ

### 3. ส่ง artifact เพิ่มถ้ามี (ไม่มีก็ตรวจได้)

Brief / Acceptance Criteria · IA หรือ Sitemap · User Flow · Design System หรือ CI ลูกค้า
ยิ่งให้มาก ยิ่งตรวจได้ลึก — ถ้าไม่มี Claude จะบอกว่าตรวจอะไรไม่ได้บ้าง **ไม่ปฏิเสธการตรวจ**

### 4. รอผล

Claude จะรัน probe ที่ 375 / 768 / 1440 / 1920 px ให้เอง แล้วออกรายงาน
ถ้าอยากรันเองก่อน (เช่นเว็บต้องล็อกอิน) — เปลี่ยน `python3` เป็น `py` ถ้าใช้ Windows:
```bash
python3 .claude/skills/web-quality-review/scripts/run-ui-probe.py <URL หรือ path ไฟล์> --out ./qa-output
```
แล้วบอก Claude ว่า `อ่าน ./qa-output/summary.md กับ shot-*.png แล้วให้คะแนนกลุ่ม UI`

---

## ได้อะไรออกมา

ไฟล์ **`report.html` เปิดได้เดี่ยวๆ** (รูปฝังเป็น base64 ไม่ต้องแนบไฟล์อื่น) ส่งต่อให้ทีมหรือลูกค้าได้เลย

- **ด้านบน** — คะแนนรวม /100 + วงกลม 🧠 UX · 🎨 UI · ⚙️ Technical + จำนวน issue แต่ละระดับ
- **แท็บ 1 ปัญหาที่ต้องแก้** — เรียงตาม Blocker / High / Medium / Low ทุกแถวบอกตำแหน่ง วิธีแก้ คะแนนที่จะได้คืน และเวลาที่ใช้
- **แท็บ 2 ผ่านแล้ว** · **แท็บ 3 ตรวจไม่ได้** (พร้อมเหตุผลและวิธีตรวจ)
- **แท็บ 4 ความพร้อม & รอบถัดไป** — readiness + งานรอบหน้า
- **แท็บ 📸 ภาพประกอบ** — screenshot 4 ขนาด + ภาพครอปจุดที่มีปัญหา

## ตรวจซ้ำรอบ 2 ขึ้นไป

ส่งรายงานรอบก่อนไปด้วย:
```
ตรวจซ้ำ https://example.com — รายงานรอบก่อนอยู่ที่ ./qa-output/r1/report.html
```
รายงานรอบซ้ำจะเพิ่ม **แท็บ 🕐 ประวัติ** เป็นไทม์ไลน์ทุกรอบ พร้อม Δ คะแนนรายกลุ่มและสิ่งที่แก้ไปแล้ว

---

## แก้ปัญหาที่เจอบ่อย

| อาการ | สาเหตุ / วิธีแก้ |
|---|---|
| กลุ่ม UI เป็น **Not Tested** ทั้งกลุ่ม | ยังไม่ได้ติดตั้ง playwright — กลับไปทำขั้นติดตั้ง |
| `command not found: python` (mac/Linux) | ใช้ `python3` ไม่ใช่ `python` |
| Windows พิมพ์ `python3` แล้วเด้ง Microsoft Store | เป็น alias เปล่าของ Windows — ใช้ `py` แทนทุกคำสั่ง |
| Windows `py` ไม่รู้จัก | ยังไม่ได้ลง Python — ลงจาก python.org แล้วติ๊ก **Add python.exe to PATH** ตอนติดตั้ง |
| Linux เปิด browser ไม่ขึ้น / ขาด `.so` | `sudo python3 -m playwright install --with-deps chromium` |
| `externally-managed-environment` ตอน pip | ใช้ venv: `python3 -m venv .venv && source .venv/bin/activate` แล้วค่อย `pip install playwright` |
| `403` / `x-deny-reason: host_not_allowed` | เน็ตมี allowlist โดเมน — ให้ส่งไฟล์ source มาเสิร์ฟ localhost แทน หรือขอ org owner เพิ่มโดเมน |
| เว็บต้องล็อกอินถึงเข้าได้ | รัน probe เองหลังล็อกอิน แล้วส่ง `qa-output/` ให้ Claude อ่าน |
| อยากได้รายงานภาษาอังกฤษ | บอกได้เลย — โครงรายงานเหมือนเดิม เปลี่ยนแค่ข้อความ |
| อัปเดตสกิลเป็นเวอร์ชันล่าสุด | `cd .claude/skills/web-quality-review && git pull` |

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

### 🟦 Product Gate — เฉพาะ Track Product (ไม่คิดคะแนน)

งาน Product เช็กเพิ่ม 5 ข้อที่เป็นเรื่อง **โจทย์และกระบวนการ** ไม่ใช่หน้าเว็บ จึงไม่เข้าสูตร /100 แต่มีผลกับคำตัดสิน

| # | เช็ก | ผ่านเมื่อ |
|---|---|---|
| P1 | สรุปโจทย์ถูกไหม | persona / journey ไม่ปนกัน · CTA ไม่ขัดกันเอง — **ไม่ผ่าน = ตีกลับ** |
| P2 | ครบจริงไหม | มี state / edge case list ให้เทียบกับผลตรวจ UX3 |
| P3 | ใช้มาตรฐานไหม | ระบุ DS + version และ pattern ที่ใช้ได้ |
| P4 | เนื้อหาเป็นของจริง | ไม่มี lorem · ตัวเลขมาจาก data จริงหรือ seed ที่ตกลงไว้ |
| P5 | ทำได้จริงไหม | ผ่าน dev BR / feasibility แล้ว — **ไม่ผ่าน = ห้ามให้ "พร้อม ship" แม้คะแนน ≥ 90** |

P1 · P3 · P5 ตรวจจาก URL อย่างเดียวไม่ได้ ต้องมี artifact — ไม่มีให้ตอบ ➖ ไม่มีข้อมูล ห้ามเดาว่าผ่าน

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
