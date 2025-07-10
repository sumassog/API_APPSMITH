from fastapi import FastAPI, File, UploadFile, Form , HTTPException
from fastapi.staticfiles import StaticFiles
import os
import uuid

app = FastAPI()

BASE_UPLOAD_FOLDER = "images/sumas_appsmith/PD"
os.makedirs(BASE_UPLOAD_FOLDER , exist_ok=True)

app.mount("/images/sumas_appsmith/PD" , StaticFiles(directory="images/sumas_appsmith/PD") , name="images/sumas_appsmith/PD")


@app.post("/postImage")
async def post_image(file: UploadFile = File(...),
                     subfolder : str = Form(...)):

    upload_path = os.path.join(BASE_UPLOAD_FOLDER , subfolder)
    
    os.makedirs(upload_path, exist_ok=True)
        
    ext = file.filename.split(".")[-1]
    unique_id = str(uuid.uuid4())
    filename = f"{unique_id}.{ext}"
    filepath = os.path.join(upload_path, filename)
        
    with open(filepath, "wb") as f:
            f.write(await file.read())
        
    public_url = f"/images/sumas_appsmith/PD/{subfolder}/{filename}"
        
    return {"url": public_url} 


@app.delete("/deleteImage")
async def delete_image(imageName : str , subFolder : str):
        
        file_path = os.path.join(BASE_UPLOAD_FOLDER + subFolder , imageName)
        if not os.path.isfile(file_path):
                raise HTTPException(status_code=404 , detail="Image not found")
        
        os.remove(file_path)
        
        return {"detail": "Image deleted"}
        
        
        