# HRAI
1. สร้าง uv และ sync library
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv sync
```
2. config `.env` เพิ่ม openai_api_key
3. รัน server 
```bash
uvicorn main:app
```
4. test resume "resume.pdf"
```bash
curl -X POST "http://localhost:8000/gradedresume/" -F  "file=@Resume.pdf" | jq .
```
