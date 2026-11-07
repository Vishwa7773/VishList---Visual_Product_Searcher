from fastapi import FastAPI,UploadFile,File,HTTPException
from src.image_search import Image_Searcher
import os
import tempfile
os.environ["TF_NUM_INTRAOP_THREADS"] = "2"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "2"
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "models" / "Fashion_products.index"
DATA_PATH = BASE_DIR / "data" / "fashion_data_5000.csv"


searcher=Image_Searcher(index_path=str(INDEX_PATH),
                         data_path=str(DATA_PATH))
app=FastAPI(title="Visual Product Search")

@app.get("/")
def home():
    return {"message" : "Visual Product Search in action!!"}


@app.post("/search")
async def find_products(file: UploadFile=File(...),k:int = 5):

    if file.content_type not in ["image/jpeg","image/jpg"]:
        raise HTTPException(400,detail="Please upload .jpeg/.jpg image")
    
    temp_path=None

    try:
        image_bytes=await file.read()
        print("Filename:", file.filename)
        print("Content type:", file.content_type)
        print("Received bytes:", len(image_bytes))
        if not image_bytes:
            raise HTTPException(status_code=500,detail='Uploaded file is empty')
        
        with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as temp_file:
            temp_path=temp_file.name
            bytes_written=temp_file.write(image_bytes)
            temp_file.flush()

            print("Bytes received:", len(image_bytes))
            print("Bytes written:", bytes_written)

            print("File size after closing:", os.path.getsize(temp_path))
            print("Temporary image path:", temp_path)
            print("Temporary image exists:", os.path.exists(temp_path))
            print("Temporary image size:", os.path.getsize(temp_path))

            if os.path.getsize(temp_path) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Temporary image file is empty."
                )
            results = searcher.search(temp_path, k)

        return {"FileName":file.filename,
                "Result_Count":len(results),
                "Results":results}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Search failed due to {e}")
    
    finally :
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        file.file.close()





    
