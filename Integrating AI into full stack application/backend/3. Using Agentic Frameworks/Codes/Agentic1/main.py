from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_selector import choose_model
from router import route_request

app = FastAPI(debug=True)

class ProductRequest(BaseModel):
    product_name: str
    tone: str

@app.post("/generate")
def generate_description(req: ProductRequest):
    try:
        prompt = {
            "text": f"Write a product description for {req.product_name} in a {req.tone} tone.",
            "tone": req.tone
        }

        selected_model = choose_model(prompt)
        output = route_request(selected_model, prompt)

        return {
            "model_used": selected_model,
            "description": output
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))