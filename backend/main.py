from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
from .data import load_dataset, profile_dataset, clean_dataset

app = FastAPI(title="AI Data Analyst API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "backend/data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/api/demo")
async def get_demo():
    file_path = os.path.join(DATA_DIR, "Supermarket_Sales.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Demo dataset not found")
    
    df = load_dataset(file_path)
    profile = profile_dataset(df)
    
    # Basic stats
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }
    
    return {
        "status": "success",
        "dataset": "Supermarket_Sales.csv",
        "profile": profile,
        "statistics": stats
    }


@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    ext = file.filename.split('.')[-1].lower()
    if ext not in ['csv', 'xlsx', 'xls']:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    file_path = os.path.join(DATA_DIR, f"uploaded_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    df = load_dataset(file_path)
    profile = profile_dataset(df)
    
    return {
        "status": "success",
        "dataset": file.filename,
        "profile": profile
    }
