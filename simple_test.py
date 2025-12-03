from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Simple AI Test")

@app.get("/")
def home():
    return {"message": "AI Agent is working!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)