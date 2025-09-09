from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

#===================== PDF Extraction ===========================
EmploymentType = Literal["Full-time", "Part-time", "Internship", "Outsource"]

class WorkExperience(BaseModel):
    title: str = Field("", description="Job title")
    company: str = Field("", description="Company or organization name")
    employment_type: EmploymentType = Field("Full-time", description="Type of employment")
    period: str = Field("", description="Total duration if available")
    achievements: List[str] = Field(default_factory=list, description="Key achievements with evidence/metrics")
    skills_gained: List[str] = Field(default_factory=list, description="Specific skills learned or strengthened from this role")


class Education(BaseModel):
    school: str = Field("", description="Educational institution name")
    degree: str = Field("", description="Degree level")
    field: str = Field("", description="Field of study")

class Skills(BaseModel):
    programming_languages: List[str] = Field(default_factory=list, description="Programming languages")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks/Libraries")
    tools: List[str] = Field(default_factory=list, description="Tools/Platforms")
    skills: List[str] = Field(default_factory=list, description="Any kind of skills")

class Resume(BaseModel):
    name: str = Field("", description="Candidate full name")
    summary: str = Field("", description="Short profile/summary or career objective")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience history")
    education: List[Education] = Field(default_factory=list, description="Education background")
    skills: Skills = Field(default_factory=Skills, description="Candidate skills")

#===================== Score ===========================
class ScoreDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: int = Field(..., ge=0, le=100, description="Score (0–100)")
    reason: str

class Scores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    education: ScoreDetail
    knowledge: ScoreDetail
    skills: ScoreDetail
    tools: ScoreDetail

Decision = Literal["strong_fit", "fit", "weak_fit", "not_fit"]

class HRState(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Important: forbid extra top-level keys
    name: str
    decision: Decision
    overall_score: int
    overall_score_reason: str =  Field(default=None, description="reason ของการให้คะแนนโดยไม่ต้องบอกวิธีการคำนวณ")
    scores: Scores
    matched: List[str]= Field(default=None, description="เฉพาะสิ่งที่ระบุไว้ใน Job description")
    missing: List[str] = Field(default=None, description="เฉพาะสิ่งที่ระบุไว้ใน Job description")