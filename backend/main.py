
# FastAPI framework and modules for file upload handling
from fastapi import FastAPI, File, UploadFile

# Imports middleware to allow cross-origin requests (CORS)
from fastapi.middleware.cors import CORSMiddleware

# Creates a FastAPI application instance
app = FastAPI()

# Configures CORS middleware to allow requests from any origin
# This is useful for development when the frontend and backend are on different ports or domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins like http://localhost:3000, http://example.com, etc.
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers like Content-Type, Authorization, etc. 
)

# Endpoint to upload a file via POST request
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Read the uploaded file's contents into memory (as bytes)
    contents = await file.read()

    # Prints the filename and size of the uploaded file to the console
    print(f"Received file: {file.filename} - size: {len(contents)} bytes")

    # Responds with the filename of the uploaded file
    return {"filename": file.filename}

# Notes:
# A cross origin request is when a frontend tries to talk to a backend that is not on the same domain or port.
# POST request is when you send data to the server, like uploading a file
# How to activate virtual environment -> bash: soucre .venv/bin/activate 
# How to run the server -> bash: uvicorn main:app --reload 

