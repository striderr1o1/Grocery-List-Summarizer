from fastapi import FastAPI, UploadFile, File, HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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