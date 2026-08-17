# 📋 ใบ 50 ทวิ

Alternatax Tool: Bai 50 Thawi generator (Streamlit)

## Run locally

```
pip install -r requirements.txt
streamlit run app.py
```

## การตั้งค่า (.env)

คัดลอก `.env.example` เป็น `.env` แล้วกรอกค่าจาก Supabase project (Project Settings → API):

- `SUPABASE_URL` — Project URL
- `SUPABASE_ANON_KEY` — anon public key (ปลอดภัยเพราะมี RLS คุมอยู่)

ดู schema เต็มที่ [acctprompt-platform](https://github.com/acctprompt-cmyk/acctprompt-platform) — ต้องรัน `schema.sql` + `seed.sql` ใน Supabase project ก่อนแอปนี้จะล็อกอินได้

ลูกค้าล็อกอินด้วย email/password ที่สมัครไว้บน Store
