# Web Quality Review

Skill สำหรับ **ตรวจคุณภาพเว็บไซต์ที่สร้างหรือแก้ไขด้วย AI ก่อนส่งมอบลูกค้า** (pre-delivery QA review)

---

## ตำแหน่งในกระบวนการทำงาน

Skill นี้คือ **Stage 5.1 Internal Test** ของ [`sellsuki-project-standard`](../sellsuki-project-standard) — ตรวจภายในให้เสร็จ *ก่อน* ส่ง staging ให้ลูกค้าทำ UAT เพื่อไม่ให้ลูกค้าเสีย UAT round ไปกับบั๊กที่ทีมควรเจอเอง

```
Stage 4 Deploy → [Stage 5.1 INTERNAL TEST ← skill นี้] → Client UAT → Stage 6 Handoff
```

UAT round budget: S = 1 · M = 2 · L = 3 รอบ

---

## รองรับ 3 ประเภทเว็บ

| | ประเภท | สัญญาณ |
|---|---|---|
| 🅐 | **Information Website** — เว็บให้ข้อมูล | เว็บบริษัท, บทความ, landing page — ผู้ใช้มาอ่าน ไม่ทำธุรกรรม |
| 🅑 | **E-Commerce** — เว็บขายสินค้า | มีสินค้า ราคา ตะกร้า ชำระเงิน จัดส่ง |
| 🅒 | **Web Application** — เว็บระบบงาน | มีล็อกอิน, dashboard, CRUD, ทำรายการหลายขั้น, สิทธิ์ตาม role |

---

## Flow การทำงานของ skill

```
ขั้น 0  ถามประเภทเว็บ + ขั้นของงาน + ขนาดโปรเจกต์   ← ห้ามข้าม
ขั้น 1  Readiness Pre-check (IA / User Flow / Design Spec / AC มีครบไหม)
ขั้น 2  รับ Input + แยก "ข้อมูลที่ได้รับ" ออกจาก "สมมติฐาน"
ขั้น 3  Core Checklist C1–C9 (ตรวจทุกประเภท)
ขั้น 4  ชุดตรวจเฉพาะประเภท (Info / E-Com / Web App)
ขั้น 5  จัดระดับความรุนแรง 4 ระดับ (Blocker / High / Medium / Low)
ขั้น 6  คิดคะแนน 100 (น้ำหนักต่างกันตามประเภท)
ขั้น 7  เขียนรายงาน
```

---

## Readiness Pre-check — artifact ที่ควรมีก่อนตรวจ

| Artifact | Info | E-Com | Web App |
|---|---|---|---|
| Project Card / Brief | ต้องมี | ต้องมี | ต้องมี |
| IA / Sitemap | **ต้องมี** | **ต้องมี** | **ต้องมี** |
| User Flow | ควรมี | **ต้องมี** (purchase flow) | **ต้องมี** (ทุก role) |
| Design Spec + variant ที่เลือก | ต้องมี | ต้องมี | ต้องมี |
| State / Edge case list | ควรมี | **ต้องมี** | **ต้องมี** |
| Test Scenario / AC | ควรมี | **ต้องมี** | **ต้องมี** |
| Mock data / API contract (Section F1) | — | **ต้องมี** | **ต้องมี** |

ถ้า artifact ไม่ครบ **ยังตรวจได้** แต่ skill จะประกาศชัดว่าหมวดไหนตรวจไม่ได้เพราะขาดเกณฑ์อ้างอิง

---

## น้ำหนักคะแนน (100 คะแนน)

| หมวด | 🅐 Info | 🅑 E-Com | 🅒 Web App |
|---|---|---|---|
| C1 Requirement & Business Goal | 15 | 15 | 15 |
| C2 IA & Navigation | 15 | 10 | 10 |
| C3 Content & Microcopy | 20 | 10 | 5 |
| C4 Visual & Design System | 15 | 10 | 10 |
| C5 Responsive | 10 | 15 | 10 |
| C6 Accessibility | 10 | 10 | 10 |
| C7 Functional QA | 5 | 5 | 10 |
| C8 Performance & SEO | 5 | 5 | 5 |
| C9 AI-Specific | 5 | 5 | 5 |
| ชุดตรวจเฉพาะประเภท | — | 15 | 20 |

**เกณฑ์ตัดสิน:** พบ Blocker ≥ 1 → ไม่ผ่านทันทีแม้คะแนนเกิน 80 · 90–100 พร้อมส่ง · 80–89 แก้ Medium ก่อน · 70–79 แก้ก่อนรอบสุดท้าย · < 70 ยังไม่ควรส่ง

---

## วิธีใช้

พิมพ์ในแชตได้เลย เช่น:
- "ตรวจเว็บนี้ก่อนส่งลูกค้าหน่อย https://..."
- "QA เว็บ [URL] ก่อนส่ง UAT"
- "รีวิวคุณภาพงานนี้" (แนบไฟล์โค้ด)

Claude จะถามประเภทเว็บและเช็ค readiness ก่อนเริ่มตรวจเสมอ

---

## Version

v1.0 — รวมจากสกิลเดิม 2 ตัว (`quality-review-checklist` ตัวเต็ม + `content-site-review` ตัวกระชับ) เป็นเวอร์ชันเดียวที่แยกตามประเภทเว็บ
