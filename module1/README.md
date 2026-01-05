# 🎓 Module 1: Dual-Model Architecture Design

> **"Understanding the Brain and Hands of AI Director"**

**Duration:** 3-4 ชั่วโมง  
**Difficulty:** ⭐⭐  
**Platform:** GitHub Codespaces

---

## 📋 Module Overview

### Learning Objectives

เมื่อจบ Module 1 คุณจะสามารถ:
- ✅ อธิบาย Dual-Model Architecture และเหตุผลที่ใช้
- ✅ เข้าใจความแตกต่างระหว่าง T5Gemma 2 (Thinker) และ FunctionGemma (Executor)
- ✅ ตัดสินใจว่าควรใช้ model ไหนสำหรับ task ไหน
- ✅ เข้าใจการทำงานร่วมกันของทั้งสอง models
- ✅ รู้จัก Smart Cut feature และการ integrate กับ architecture
- ✅ สร้าง AI Director Agent แบบ basic ได้

### Prerequisites

- GitHub account (สำหรับ Codespaces)
- ความเข้าใจพื้นฐานเกี่ยว LLM และ AI models
- Python basics

---

## 📁 Module Structure

```
module1/
├── README.md                      (ไฟล์นี้)
├── requirements.txt               (Dependencies)
├── 01_t5gemma_thinker.py         (T5Gemma 2 implementation)
├── 02_functiongemma_executor.py   (FunctionGemma implementation)
├── 03_ai_director_agent.py        (Complete dual-model agent)
├── 04_test_module1.py             (Testing script)
└── examples/
    ├── example_strategy.py        (Strategy generation example)
    ├── example_tool_calling.py    (Tool calling example)
    └── example_smart_cut.py       (Smart Cut workflow example)
```

---

## 🚀 Quick Start

### 1. ติดตั้ง Dependencies

```bash
cd module1
pip install -r requirements.txt
```

### 2. ทดสอบ T5Gemma 2 (Thinker)

```bash
python 01_t5gemma_thinker.py
```

### 3. ทดสอบ FunctionGemma (Executor)

```bash
python 02_functiongemma_executor.py
```

### 4. ทดสอบ Complete Agent

```bash
python 03_ai_director_agent.py
```

### 5. Run Tests

```bash
python 04_test_module1.py
```

---

## 📚 Learning Path

### Part 1: Why Dual-Model Architecture?
- เข้าใจปัญหาของ single large model
- ทำไมต้องแยก "Thinking" และ "Executing"
- Cost, Speed, Reliability comparison

### Part 2: T5Gemma 2 (The Thinker)
- Architecture และ capabilities
- Use cases: Strategy, Content, Analysis
- Hands-on: Generate marketing strategy

### Part 3: FunctionGemma (The Executor)
- Specialized for tool calling
- Use cases: Parse, Call, Orchestrate
- Hands-on: Parse to tool calls

### Part 4: Integration
- Communication protocol
- Workflow design
- Error handling

### Part 5: Smart Cut Integration
- Video editing workflow
- Highlight selection
- Automated cutting

---

## ✅ Completion Criteria

Check ทุกข้อก่อนไป Module 2:

### Understanding (ทฤษฎี)
- [ ] อธิบายได้ว่าทำไมใช้ dual-model แทน single large model
- [ ] อธิบายความแตกต่างระหว่าง T5Gemma 2 และ FunctionGemma ได้
- [ ] บอกได้ว่า task ไหนควรใช้ model ไหน
- [ ] เข้าใจ communication protocol ระหว่าง 2 models

### Practical (ลงมือทำ)
- [ ] Load T5Gemma 2 และ generate text ได้
- [ ] Load FunctionGemma และ parse tool calls ได้
- [ ] สร้าง AI Director Agent ที่ใช้ทั้ง 2 models ได้
- [ ] ออกแบบ workflow สำหรับ use case หนึ่ง

### Smart Cut (ใหม่)
- [ ] เข้าใจว่า Smart Cut ใช้ dual-model architecture อย่างไร
- [ ] อธิบายได้ว่าทำไม T5Gemma 2 เหมาะสำหรับเลือก highlights
- [ ] เข้าใจบทบาทของ FunctionGemma ในการควบคุม FFmpeg

---

## 📝 Knowledge Check

### Quiz Questions

1. **ทำไม AI Director ใช้ 2 models แทน 1 large model?**
   - A. ถูกกว่า
   - B. เร็วกว่า
   - C. แม่นกว่า
   - D. ถูกทุกข้อ ✅

2. **T5Gemma 2 ใช้ architecture แบบไหน?**
   - A. Encoder-only
   - B. Decoder-only
   - C. Encoder-Decoder ✅
   - D. Mixture of Experts

3. **FunctionGemma มี parameters กี่ตัว?**
   - A. 1B
   - B. 270M ✅
   - C. 7B
   - D. 70B

4. **Task ไหนควรใช้ T5Gemma 2?**
   - A. Parse JSON
   - B. Call API
   - C. เขียน marketing copy ✅
   - D. ถูกทุกข้อ

5. **Smart Cut ใช้ T5Gemma 2 ทำอะไร?**
   - A. Transcribe audio
   - B. Detect silence
   - C. Select highlights ✅
   - D. Cut video

---

## 🔗 Related Resources

- [T5Gemma 2 Documentation](https://huggingface.co/google/t5gemma-2-1b-1b)
- [FunctionGemma Documentation](https://huggingface.co/google/functiongemma-270m-it)
- [Course Documentation](../course_ai-assistant_v3.4.2.md)

---

## 🎯 Next Steps

เมื่อเสร็จ Module 1 แล้ว:
- ไปต่อที่ **Module 2: ETL Pipeline**
- ทำ Final Project: สร้าง complete AI Director pipeline

---

**Happy Learning! 🚀**
