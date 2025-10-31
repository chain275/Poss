# AI-POS

เป็นระบบสั่งอาหารด้วยเสียง โดยใช้ large language model (llm) ของ Deepseek ในการทำความเข้าใจและคิดคำสื่อสารเพื่อโด้ตอบกับลูกค้า พร้อมกับใช้ automatic speech recognition(ASR) ของ Typhoon เพื่อจับคำพูดของลูกค้า ตอบโต้แบบสนทนาในภาษาไทย มีฟีเจอร์ในการจดออเดอร์(POS)

## Features

Cashier.py:
- ระบบ POS (Point-of-sale)
- รับอินพุธจาก Deepseek.py

ASR/:
- รับอินพุธจากไมโครโฟน และ ตัดประโยคออกจากไฟล์เสียง และ ส่งไปที่ Typhoon API

Deepseek.py:
- ใช้แปลง Natural language เป็นการจดออเดอร์ และส่งเอาท์พุธไปที่ Cashier.py


db_manager.py:
- สร้าง SQLite Database เพื่อใช้ในการเก็บข้อมูล เมนู ราคา




## Installation

Install the required libraries using [uv](https://docs.astral.sh/uv/)
```bash
git clone https://github.com/yourusername/myproject.git
cd myproject
uv sync
```
## Requirement

1. Deepseek api key
2. Typhoon api key
