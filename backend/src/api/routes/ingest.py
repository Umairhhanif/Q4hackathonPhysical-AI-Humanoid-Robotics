from fastapi import APIRouter, HTTPException, Depends, Header
from src.core.config import settings
from src.services.ingest import ingest_documents
from src.models.api import IngestResponse
import os

router = APIRouter()

async def verify_secret(x_api_key: str = Header(...)):
    if x_api_key != settings.API_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@router.post("/ingest", response_model=IngestResponse, dependencies=[Depends(verify_secret)])
async def trigger_ingest():
    # Assuming docs are in /website/docs or just /docs relative to repo root
    # We need to find the repo root. 
    # Current working dir is E:\software\Speckithackhaton
    # So docs are likely in E:\software\Speckithackhaton\website\docs
    
    # Try to locate docs directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
    docs_dir = os.path.join(base_dir, "website", "docs")
    
    if not os.path.exists(docs_dir):
        # Fallback for dev environment structure
        docs_dir = os.path.join(base_dir, "docs")
        
    if not os.path.exists(docs_dir):
         raise HTTPException(status_code=404, detail=f"Docs directory not found at {docs_dir}")

    try:
        count = await ingest_documents(docs_dir)
        return IngestResponse(
            status="success",
            chunks_processed=count,
            message="Ingestion completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
