import fitz
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import uvicorn
from state import Resume,HRState

load_dotenv()
app = FastAPI()

def pdf_to_text(file_bytes: bytes) -> str:
    """แปลง PDF -> ข้อความ (ลอง text ก่อน, ไม่มีก็ค่อย OCR)"""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    try:
        texts = []
        for page in doc:
            txt = page.get_text("text") or ""
            if txt.strip():
                texts.append(txt)
            else:
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_txt = pytesseract.image_to_string(img, lang="tha+eng")
                texts.append(ocr_txt)
        return "\n".join(texts).strip()
    finally:
        doc.close()

def getpath(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

JB_DES_TXT = Path("Job_description/AI.txt").read_text(encoding="utf-8")
LLM_RESUME = ChatOpenAI(model="gpt-4o-mini")
PROMPT_RESUME_TMPL = ChatPromptTemplate.from_template(getpath("prompt/to_json_pmt.txt"))
LLM_HR = ChatOpenAI(model="gpt-5-mini")
PROMPT_HR_TMPL = ChatPromptTemplate.from_template(getpath("prompt/hr_pmt.txt"))

@app.post("/gradedresume/")
async def gradedResume(file: UploadFile = File(...)):
    try:
        if file.content_type not in {"application/pdf"}:
            raise HTTPException(status_code=415, detail="รองรับเฉพาะไฟล์ PDF")

        file_bytes = await file.read()
        text = pdf_to_text(file_bytes)

        prompt_resume = PROMPT_RESUME_TMPL.format_messages(text=text)
        sllm_resume = LLM_RESUME.with_structured_output(Resume)
        resume_state: Resume = sllm_resume.invoke(prompt_resume)

        prompt_hr = PROMPT_HR_TMPL.format_messages(ResumeState=resume_state, Job_des=JB_DES_TXT)
        sllm_hr = LLM_HR.with_structured_output(HRState)
        result: HRState = sllm_hr.invoke(prompt_hr)

        return JSONResponse(content=result.model_dump())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)