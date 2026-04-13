from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.inference_engine import InferenceEngine
import logging

app = FastAPI(
    title="InsightFlow",
    description="AI-powered customer intent analyzer",
    version="1.0.0"
)

# Initialize the inference engine
inference_engine = InferenceEngine()

class TicketRequest(BaseModel):
    ticket_text: str
    customer_id: str = None

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    sentiment: str
    customer_id: str = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/v1/analyze-intent", response_model=IntentResponse)
async def analyze_intent(request: TicketRequest):
    """
    Analyze customer ticket intent using AI models.
    """
    try:
        logger.info(f"Analyzing intent for customer: {request.customer_id}")

        # Analyze sentiment and intent
        result = inference_engine.analyze_ticket(request.ticket_text)

        response = IntentResponse(
            intent=result.get("intent", "unknown"),
            confidence=result.get("confidence", 0.0),
            sentiment=result.get("sentiment", "neutral"),
            customer_id=request.customer_id
        )

        logger.info(f"Analysis complete for customer {request.customer_id}: {response.intent}")
        return response

    except Exception as e:
        logger.error(f"Error analyzing intent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "InsightFlow"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)