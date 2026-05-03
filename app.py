from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RequestData(BaseModel):
    company_name: str
    url: str
    source: str
    model_name: str

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/generate")
def generate(data: RequestData):
    try:
        from brochureGenerator import create_brochure  # lazy import

        result = create_brochure(
            data.company_name,
            data.url,
            data.source,
            data.model_name
        )

        return {"output": result}

    except Exception as e:
        return {"error": str(e)}