from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
from app.utils.s3 import upload_file_to_s3

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("", response_model=Dict[str, str])
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to S3.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Upload to S3
    url = upload_file_to_s3(file.file, file.filename, file.content_type)
    
    if not url:
        raise HTTPException(status_code=500, detail="Failed to upload file")
        
    return {"url": url}
