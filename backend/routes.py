from fastapi import APIRouter, UploadFile, File, Form
import pdfplumber
import io

from backend.agents.image_agent import run_image_sampling_agent
from backend.agents.planner import run_planner_agent
from backend.agents.executer import calculate_progress  
from backend.data.segments import TOTAL_SEGMENTS

from backend.graph.workflow import workflow

from pydantic import BaseModel


# -------------------------
# RESPONSE SCHEMA
# -------------------------
class MilestoneVerificationResponse(BaseModel):
    expected_progress: float
    actual_progress: float
    progress_match: bool
    deadline: str
    deadline_ok: bool
    quality_verified: bool
    milestone_verified: bool
    decision: str


router = APIRouter()

current_contract_data = {}

# In-memory progress store (prototype)
verified_segment_ids = set()


# -------------------------
# CONTRACT UPLOAD
# -------------------------
@router.post("/upload-contract")
async def upload_contract(file: UploadFile = File(...)):
    global current_contract_data

    pdf_bytes = await file.read()
    text = ""

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    current_contract_data = {
        "contract_text": text
    }

    return {"status": "contract_uploaded"}


# -------------------------
# IMAGE + SAMPLING UPLOAD
# -------------------------
@router.post("/upload-progress-image")
async def upload_progress_image(
    image: UploadFile = File(...),
    segment_id: str = Form(...),
    segment_index: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    timestamp: str = Form(...)
):
    image_bytes = await image.read()

    agent_output = run_image_sampling_agent(
        image_bytes=image_bytes,
        segment_id=segment_id,
        segment_index=segment_index,
        latitude=latitude,
        longitude=longitude,
        timestamp=timestamp,
        contractor_risk_level="NORMAL"
    )

    if agent_output["geo_valid"]:
        verified_segment_ids.add(segment_id)

    progress = calculate_progress(
        verified_segments=len(verified_segment_ids),
        total_segments=TOTAL_SEGMENTS
    )

    return {
        "image_agent_output": agent_output,
        "verified_segments": len(verified_segment_ids),
        "progress_percent": progress
    }


# -------------------------
# MILESTONE VERIFICATION (LANGGRAPH)
# -------------------------
@router.get(
    "/verify-milestone",
    response_model=MilestoneVerificationResponse
)
async def verify_milestone_endpoint():
    if not current_contract_data:
        return {"error": "No contract uploaded"}

    if not verified_segment_ids:
        return {"error": "No verified progress data"}

    result = workflow.invoke({
        "contract_text": current_contract_data["contract_text"],
        "verified_segments": len(verified_segment_ids)
    })

  
    return result["verification_result"]
