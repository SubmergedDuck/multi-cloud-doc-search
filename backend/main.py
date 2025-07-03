# Imports the io module for handling byte streams and os interactions
import io 
import os

# FastAPI framework and modules for file upload handling
from fastapi import FastAPI, File, UploadFile

# Imports middleware to allow cross-origin requests (CORS)
from fastapi.middleware.cors import CORSMiddleware

from google.cloud import storage
from PyPDF2 import PdfReader 

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

# GCS bucket name matching my Terraform config
BUCKET_NAME = "duckcloud-docsearch-bucket"

# Initializes a GCS client to interact with Google Cloud Storage, this client will be used to upload files to the specified bucket
storage_client = storage.Client()

# Endpoint to upload a file via POST request
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Read the uploaded file's contents into memory (as bytes)
    contents = await file.read() 

    # Gets the bucket from GCS
    bucket = storage_client.bucket(BUCKET_NAME)

    # Creates a blob (object) in the bucket with the filename from the uploaded file
    blob = bucket.blob(file.filename)

    # Uploads the file contents GCS
    blob.upload_from_string(contents, content_type=file.content_type)

    return {
        "message": f"File '{file.filename}' uploaded to bucket '{BUCKET_NAME}'",
        "gcs_url": f"gs://{BUCKET_NAME}/{file.filename}"
    }

# Endpoint to extract text from a PDF file via POST request
@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):

    # Reads the uploaded PDF file's contents into memory
    contents = await file.read()

    stream = io.BytesIO(contents)

    # Creates a PdfReader object from the byte stream of the PDF file
    reader = PdfReader(stream)

    extracted_text = ""

    # Loops through each page in the PDF and extracts text (if any)
    for page in reader.pages:

        # page.extract_text() returns a string or None
        extracted_text += page.extract_text() or ""

    # Returns the extracted text as a JSON response    
    return {"text": extracted_text.strip()}


# Notes:
# A cross origin request is when a frontend tries to talk to a backend that is not on the same domain or port.
# POST request is when you send data to the server, like uploading a file
# io.BytesIO is used to create a byte stream from the file contents
# A byte stream is like a file but in RAM
# The strip() method is used to remove any leading or trailing whitespace from the extracted text

# How to activate virtual environment -> bash: source .venv/bin/activate 
# How to run the server -> bash: uvicorn main:app --reload -> http://localhost:8000/, http://127.0.0.1:8000/docs 

# Setting up GCP Credentials:
# gcp auth application-default login

# API Documentation Notes:
# PyPDF2: https://pypdf2.readthedocs.io/en/3.0.0/modules/PdfReader.html
# fastapi: https://fastapi.tiangolo.com/tutorial/request-files/