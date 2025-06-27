
# FastAPI framework and modules for file upload handling
from fastapi import FastAPI, File, UploadFile

# 
from fastapi.middleware.cors import CORSMiddleware

# Creates a FastAPI application instance
app = FastAPI()

# Frontend or testing from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# I want to make a test change yay!!
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    print(f"Received file: {file.filename} - size: {len(contents)} bytes")
    return {"filename": file.filename}