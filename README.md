# Web Quality Review

Skill สำหรับ **ตรวจคุณภาพงานเว็บ/UI ที่สร้างหรือแก้ไขด้วย AI ก่อนส่งมอบ** (pre-delivery QA review)

แบ่งการตรวจ **2 มิติ** — Track (Product / Project) × ประเภทเว็บ (Info / E-Commerce / Web App)

---

## ตำแหน่งในกระบวนการทำงาน

Skill นี้คือ **ด่านตรวจภายในก่อนปล่อยงาน** ของทั้งสอง track — อ้างอิง [BearyCenter/uxui](https://github.com/BearyCenter/uxui)

```
🟦 Product track  (sellsuki-product-standard)
Stage 0 Intake → 1 Research → 2 Design → 3 AI Usability → 4 Refine → 5 Vibe Code
                                                          → [QA REVIEW ← skill นี้] → merge/ship → measure → loop กลับ Stage 0

🟨 Project track  (sellsuki-project-standard)
Stage 0 Brief → 1 Research & Plan → 2 Vibe Design → 3 Vibe Code → 4 Deploy
                          → [QA REVIEW ← skill นี้ = Stage 5.1 Internal Test] → Client UAT → 6 Handoff → hard stop
```

Project track มี UAT round budget จำกัด (S=1, M=2, L=3) — ตรวจภายในให้เสร็จก่อน เพื่อไม่ให้ลูกค้าเสีย round ไปกับบั๊กที่ทีมควรเจอเอง

---

## 2 มิติของการตรวจ

### มิติที่ 1 — Track

| Track | ใช้กับ | สัญญาณ | จบงานแบบไหน |
|---|---|---|---|
| 🟦 **Product** | Sellsuki core platform, internal tools, ของที่เราเป็นเจ้าของและ iterate ต่อ | Jira key `SUKI` `OC` `MNG` · label `product` `internal` `core` | **Loop** — ship แล้ววัดผล กลับ Stage 0 |
| 🟨 **Project** | งานลูกค้า, one-off, integration จบในตัว | Jira key `CLIENT-XXX` · label `client` `project` `delivery` | **Hard stop** — ส่งมอบ + handoff |

ถ้าไม่แน่ใจ → default = Product แต่ต้อง confirm ก่อนเริ่มตรวจ

### มิติที่ 2 — ประเภทเว็บ

| | ประเภท | สัญญาณ |
|---|---|---|
| 🅐 | **Information Website** — เว็บให้ข้อมูล | เว็บบริษัท, บทความ, landing page — ผู้ใช้มาอ่าน |
| 🅑 | **E-Commerce** — เว็บขายสินค้า | มีสินค้า ราคา ตะกร้า ชำระเงิน |
| 🅒 | **Web Application** — เว็บระบบงาน | ล็อกอิน, dashboard, CRUD, ทำรายการหลายขั้น, role |

สองมิติแยกกันอิสระ — งาน Product ส่วนใหญ่เป็น 🅒 แต่ก็มี Product + 🅐 ได้ (เช่น marketing page ของ Sellsuki เอง)

---

## Flow การทำงานของ skill

```
ขั้น 0  ถาม Track + ประเภทเว็บ + ขนาดงาน            ← ห้ามข้าม
ขั้น 1  Readiness Pre-check (artifact ต่างกันตาม track)
ขั้น 2  รับ Input + แยก "ข้อมูลที่ได้รับ" ออกจาก "สมมติฐาน"
ขั้น 3  Core Checklist C1–C10 (ตรวจทุก track ทุกประเภท)
ขั้น 4  ชุดตรวจเฉพาะประเภทเว็บ
ขั้น 5  ชุดตรวจเฉพาะ Track
ขั้น 6  จัดระดับความรุนแรง 4 ระดับ (Blocker / High / Medium / Low)
ขั้น 7  คิดคะแนน 100
ขั้น 8  เขียนรายงาน
```

---

## Readiness Pre-check — artifact ต่างกันตาม track

### 🟦 Product track
| Artifact | S | M | L |
|---|---|---|---|
| Intake Brief + Acceptance Criteria | ต้องมี | ต้องมี | ต้องมี |
| Research Journey | ➖ | ควรมี | **ต้องมี** |
| IA / Wireframe Spec | ต้องมี | ต้องมี | **ต้องมี** + sitemap |
| Persona Test Result (AI Usability) | ➖ | **ต้องมี** 1–2 | **ต้องมี** 3+ |
| Must-fix list ปิดครบ | ➖ | **ต้องมี** | **ต้องมี** |
| Design Spec (final) + DS choice (DS1/DS2) | ต้องมี | ต้องมี | ต้องมี |

### 🟨 Project track
| Artifact | Info | E-Com | Web App |
|---|---|---|---|
| Project Card / Brief | ต้องมี | ต้องมี | ต้องมี |
| IA / Sitemap | **ต้องมี** | **ต้องมี** | **ต้องมี** |
| User Flow | ควรมี | **ต้องมี** | **ต้องมี** (ทุก role) |
| Design Spec + variant ที่ลูกค้าเลือก | ต้องมี | ต้องมี | ต้องมี |
| State / Edge case list | ควรมี | **ต้องมี** | **ต้องมี** |
| Staging URL + Deploy checklist | ต้องมี | ต้องมี | ต้องมี |
| Test Scenario / AC | ควรมี | **ต้องมี** | **ต้องมี** |
| Handoff Section F (F1 backend, F2 QA) | — | **ต้องมี** | **ต้องมี** |

ถ้า artifact ไม่ครบ **ยังตรวจได้** แต่ skill จะประกาศชัดว่าหมวดไหนตรวจไม่ได้เพราะขาดเกณฑ์อ้างอิง

---

## ชุดตรวจเฉพาะ Track (ต่างกันชัดเจน)

| 🟦 Product — กลืนกับ platform เดิม ไม่ทำของเดิมพัง วัดผลได้ | 🟨 Project — ตรงที่ตกลงกับลูกค้า ส่งมอบครบ ไม่มีของค้าง |
|---|---|
| DS version ถูก (DS1/DS2) ตรง module | ตรง CI/Brand ลูกค้าทุกค่า |
| ใช้ DS component จริง (`ssk-*`) ไม่สร้างใหม่ | ทำตาม variant ที่ลูกค้าเลือก |
| ใช้ DS token เท่านั้น ไม่ hardcode | Scope ตรง project card ไม่ขาดไม่เกิน |
| กลืนกับ pattern ของหน้าจอเดิม | UAT readiness (staging, deploy checklist) |
| Regression — shared component ไม่ทำที่อื่นพัง | Improvement log ปิดครบ |
| Must-fix จาก Persona Test ปิดครบ | Handoff Section F1/F2 พร้อม |
| AC จาก Jira card ครบทุกข้อ | สิทธิ์การใช้ asset (รูป/ฟอนต์) |
| Measure hook / analytics พร้อม | ไม่มีร่องรอยงานภายในหลุด |
| Rollout safety (feature flag / rollback) | หน้ากฎหมายที่ลูกค้าต้องมี |
| ไม่ทิ้ง design debt แบบเงียบ | ส่งมอบ domain/hosting/credential |
| i18n ถ้า platform รองรับหลายภาษา | Post-launch report พร้อมร่าง |

---

## น้ำหนักคะแนน (100 คะแนน)

| หมวด | 🅐 Info | 🅑 E-Com | 🅒 Web App |
|---|---|---|---|
| C1 Requirement & Business Goal | 12 | 12 | 12 |
| C2 IA & Navigation | 12 | 8 | 8 |
| C3 Content & Microcopy | 12 | 8 | 4 |
| C4 Visual & Component Consistency | 12 | 8 | 8 |
| C5 States ครบ (6 states ตามกฎ Q1) | 4 | 8 | 8 |
| C6 Responsive | 8 | 12 | 8 |
| C7 Accessibility | 8 | 8 | 8 |
| C8 Functional QA | 4 | 4 | 8 |
| C9 Performance & SEO | 4 | 4 | 3 |
| C10 AI-Specific | 4 | 4 | 3 |
| ชุดเฉพาะประเภทเว็บ | 5 | 9 | 15 |
| **ชุดเฉพาะ Track** | **15** | **15** | **15** |

### เกณฑ์ตัดสิน (ถ้อยคำต่างกันตาม track)

| คะแนน | 🟦 Product | 🟨 Project |
|---|---|---|
| พบ Blocker ≥ 1 | 🚫 ห้าม merge/ship | 🚫 ห้ามส่งลูกค้า |
| 90–100 | ✅ พร้อม merge / ship | ✅ พร้อมส่งลูกค้า UAT |
| 80–89 | ⚠️ ship ได้ ควรแก้ Medium | ⚠️ ส่งได้ ควรแก้ Medium |
| 70–79 | 🔧 ต้องแก้ก่อน merge | 🔧 ต้องแก้ก่อนรอบสุดท้าย |
| < 70 | 🚫 ยังไม่ควร ship | 🚫 ยังไม่ควรส่งมอบ |

---

## การติดตั้ง

### Claude Code (แนะนำ — อ่านโค้ดจริงได้)
```bash
cd path/to/your-project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/Krittiya-Amm/web-quality-review.git
```
แล้ว commit ลง git ของโปรเจกต์ → ทั้งทีมที่ pull ได้สกิลไปด้วย

### claude.ai
Customize > Skills > "+" > Upload a skill → อัป ZIP ที่มีโฟลเดอร์ `web-quality-review/` เป็นราก
(ต้องเปิด Code execution and file creation ใน Settings > Capabilities ก่อน)

---

## การเรียกใช้

```
/web-quality-review
```
หรือพิมพ์ธรรมดา เช่น "ตรวจงานนี้ก่อน merge หน่อย" / "QA เว็บนี้ก่อนส่งลูกค้า https://..."

Claude จะถาม track และประเภทเว็บ แล้วเช็ค readiness ก่อนเริ่มตรวจเสมอ

**คำศัพท์ที่ใช้ให้ตรงกัน:** ติดตั้ง (setup ครั้งเดียว) · เรียกใช้ (ทุกครั้งที่ตรวจ) · อัปเดต (`git pull`) · แชร์ (ส่งรีโปให้คนอื่นติดตั้ง)

---

## Version

**v2.0** — เพิ่มมิติ Product/Project track, Core ขยายเป็น C1–C10 (แยก States เป็นหมวดของตัวเองตามกฎ Q1), ชุดตรวจเฉพาะ track, เกณฑ์ตัดสินแยกตาม track
v1.0 — รวมสกิลเดิม 2 ตัว เป็นเวอร์ชันเดียวที่แยกตามประเภทเว็บ
