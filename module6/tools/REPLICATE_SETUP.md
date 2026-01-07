# Replicate API Token Setup Guide

## 🚀 Quick Setup (5 นาที)

### Step 1: สร้างบัญชี Replicate

1. ไปที่ https://replicate.com
2. คลิก **"Sign up"** มุมขวาบน
3. สมัครด้วย:
   - GitHub account (แนะนำ - เร็วที่สุด)
   - Google account
   - Email

### Step 2: รับ API Token

1. หลังจาก login แล้ว ไปที่: https://replicate.com/account/api-tokens
2. คลิก **"Create token"** 
3. ตั้งชื่อ token (เช่น "flying-car-ad-generator")
4. คัดลอก token (ขึ้นต้นด้วย `r8_...`)
   - ⚠️ **สำคัญ**: เก็บ token ไว้ปลอดภัย จะแสดงครั้งเดียว!

### Step 3: ตั้งค่า Token ใน VS Code

**Option 1: Environment Variable (แนะนำ)**

```bash
# Linux/Mac/DevContainer
export REPLICATE_API_TOKEN="r8_your_token_here"

# Windows PowerShell
$env:REPLICATE_API_TOKEN="r8_your_token_here"

# Windows CMD
set REPLICATE_API_TOKEN=r8_your_token_here
```

**Option 2: ใส่ใน .env file**

```bash
# สร้างไฟล์ .env ใน module7/
cd /workspaces/second-brain-ai-assistant-course/module7
echo "REPLICATE_API_TOKEN=r8_your_token_here" > .env
```

**Option 3: ใส่ตรงในโค้ด (ไม่แนะนำ - สำหรับทดสอบเท่านั้น)**

```python
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_your_token_here"
```

### Step 4: ทดสอบ Token

```bash
cd /workspaces/second-brain-ai-assistant-course/module7

python3 -c "
import os
import sys
sys.path.insert(0, '../module6/tools')

token = os.environ.get('REPLICATE_API_TOKEN')
if token:
    print(f'✅ Token found: {token[:10]}...')
    
    # Test with Replicate API
    from replicate_image_generator import ReplicateImageGenerator
    
    generator = ReplicateImageGenerator(api_token=token)
    print('✅ Generator initialized successfully!')
else:
    print('❌ Token not found. Please set REPLICATE_API_TOKEN')
"
```

## 💰 ราคาและ Credit

**⚠️ Replicate ไม่มี Free Tier:**
- ❌ ไม่มี free credit เมื่อสมัคร
- 💳 **ต้องเติมเงินก่อนใช้งาน**
- 💵 เติมขั้นต่ำ: $5
- 🔗 เติมที่: https://replicate.com/account/billing#billing

**ราคา per image:**
- SDXL: ~$0.003 (3 สตางค์/รูป) → $5 = ~1,600 รูป
- SDXL Lightning: ~$0.001 (1 สตางค์/รูป) → $5 = ~5,000 รูป

## 🎬 ทดสอบสร้างรูปจริง

```bash
cd /workspaces/second-brain-ai-assistant-course/module7

python3 -c "
import sys
import os
sys.path.insert(0, '../module6/tools')

os.environ['REPLICATE_API_TOKEN'] = 'r8_your_token_here'  # ใส่ token ของคุณ

from replicate_image_generator import ReplicateImageGenerator

generator = ReplicateImageGenerator(model='sdxl')

print('🎨 Generating flying car image...')
image = generator.generate(
    prompt='A futuristic flying car soaring through clouds, sleek aerodynamic design, photorealistic, 8k, cinematic lighting',
    width=1024,
    height=1024,
    output_file='test_flying_car.png'
)
print('✅ Image saved to test_flying_car.png')
"
```

## 🔒 Security Best Practices

1. **ห้าม commit token** ลง git
   - เพิ่ม `.env` ใน `.gitignore`
   
2. **ใช้ environment variables**
   - ไม่ hard-code ในโค้ด

3. **Rotate tokens** เป็นประจำ
   - Delete old tokens ที่ไม่ใช้แล้ว

4. **Monitor usage**
   - เช็คที่ https://replicate.com/account

## 🚨 Troubleshooting

### ❌ "No API token found"
```bash
# ตรวจสอบว่าตั้งค่าถูกต้อง
echo $REPLICATE_API_TOKEN

# ถ้าว่าง ให้ตั้งค่าใหม่
export REPLICATE_API_TOKEN="r8_your_token_here"
```

### ❌ "403 Forbidden"
- Token ไม่ถูกต้อง → สร้าง token ใหม่
- Token หมดอายุ → สร้าง token ใหม่

### ❌ "Insufficient credits" (402 Error)
- **ต้องเติมเงิน**: https://replicate.com/account/billing#billing
- เติมขั้นต่ำ $5
- รอ 2-3 นาที หลังเติมเงิน
- ⚠️ Replicate ไม่มี free tier

## 📚 Resources

- Replicate Dashboard: https://replicate.com/account
- API Docs: https://replicate.com/docs
- Models: https://replicate.com/explore
- Pricing: https://replicate.com/pricing

---

**Ready to generate real AI images! 🎨**
