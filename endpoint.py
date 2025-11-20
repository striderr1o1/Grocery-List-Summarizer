from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.post("/uploadfile")
def uploadFile(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("image.jpeg", 'wb') as f:
            f.write(contents)
        
    except Exception:
        raise HTTPException(500, detail="Something went wrong")