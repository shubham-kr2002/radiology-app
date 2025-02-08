from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Radiology AI Server is Running!"}
