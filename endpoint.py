from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use specific origin in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/uploadfile")
def uploadFile(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("image.jpeg", 'wb') as f:
            f.write(contents)
        return {"message": "File uploaded successfully"}
        
    except IOError as e:
        logger.error(f"IOError saving file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")