from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Age Check API Running"}
    
@app.get("/health")
    
def health():
    return {"status" : "ok"}