# InsightFlow

An AI-powered customer intent analyzer that uses open-source large language models to analyze CRM ticket text and determine customer intent, sentiment, and satisfaction levels.

## Architecture Overview

InsightFlow implements a decoupled, microservices-ready architecture that separates concerns for scalability and maintainability:

### Decoupled Architecture

- **API Layer (FastAPI)**: RESTful endpoints for ticket analysis
- **Inference Engine**: Isolated AI model processing with Hugging Face Transformers
- **Containerization**: Docker-based deployment for consistent environments

### Key Components

```
InsightFlow/
├── app/
│   ├── main.py                 # FastAPI application & endpoints
│   └── services/
│       └── inference_engine.py # AI model inference logic
├── Dockerfile                  # Container build configuration
├── docker-compose.yml          # Local orchestration
├── requirements.txt            # Python dependencies
└── README.md
```

## AI Model: Open-Source LLM for CRM Intent Analysis

InsightFlow leverages **CardiffNLP Twitter RoBERTa Base Sentiment** - a lightweight, open-source transformer model fine-tuned for sentiment analysis. This model provides:

### Model Capabilities

- **Sentiment Classification**: Analyzes text to determine positive, negative, or neutral sentiment
- **Confidence Scoring**: Provides probability scores for sentiment predictions
- **Intent Derivation**: Uses rule-based logic combined with sentiment to classify customer intent

### Why This Model?

- **Lightweight**: ~500MB model size, suitable for containerized deployment
- **Fast Inference**: Optimized for real-time analysis of customer tickets
- **Open-Source**: No API costs, full transparency, and community support
- **Fine-Tuned**: Specifically trained on social media data, applicable to customer feedback

### Intent Classification Logic

The system combines sentiment analysis with keyword-based rules to classify customer intent:

- **Complaint**: Negative sentiment + problem-related keywords
- **Inquiry**: Question words + neutral sentiment
- **Praise**: Positive sentiment + appreciation keywords
- **Feature Request**: Suggestion keywords + neutral/positive sentiment
- **General Feedback**: Default classification

## API Endpoints

### POST `/api/v1/analyze-intent`

Analyzes customer ticket text for intent and sentiment.

**Request:**
```json
{
  "ticket_text": "The product stopped working after the update. Very disappointed!",
  "customer_id": "CUST-12345"
}
```

**Response:**
```json
{
  "intent": "complaint",
  "confidence": 0.987,
  "sentiment": "negative",
  "customer_id": "CUST-12345"
}
```

### GET `/health`

Service health check endpoint.

## Setup & Deployment

### Prerequisites

- Docker and Docker Compose
- 4GB+ RAM (for model loading)
- Internet connection (for initial model download)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd InsightFlow
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Verify deployment**
   ```bash
   curl http://localhost:8000/health
   ```

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage Examples

### Complaint Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze-intent \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_text": "The app crashes every time I try to save. This is unacceptable!",
    "customer_id": "CUST-001"
  }'
```

**Response:**
```json
{
  "intent": "complaint",
  "confidence": 0.945,
  "sentiment": "negative",
  "customer_id": "CUST-001"
}
```

### Inquiry Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze-intent \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_text": "How do I reset my password? Can you help me?",
    "customer_id": "CUST-002"
  }'
```

**Response:**
```json
{
  "intent": "inquiry",
  "confidence": 0.823,
  "sentiment": "neutral",
  "customer_id": "CUST-002"
}
```

### Praise Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze-intent \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_text": "Love the new features! The app is amazing now.",
    "customer_id": "CUST-003"
  }'
```

**Response:**
```json
{
  "intent": "praise",
  "confidence": 0.967,
  "sentiment": "positive",
  "customer_id": "CUST-003"
}
```

## Performance Considerations

### Model Loading
- Initial model download: ~500MB
- Loading time: ~30-60 seconds on first run
- Memory usage: ~2GB RAM during inference

### Inference Speed
- Average processing time: 200-500ms per ticket
- Batch processing: Not currently implemented (single ticket analysis)
- GPU acceleration: Not enabled (CPU-only for container compatibility)

### Scalability
- Containerized deployment allows horizontal scaling
- Stateless design supports load balancing
- Model caching prevents repeated downloads

## Configuration

### Environment Variables

```bash
# Model configuration
MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest

# Server configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Model Customization

To use a different sentiment model, modify `inference_engine.py`:

```python
self.sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="your-custom-model",
    tokenizer="your-custom-tokenizer"
)
```

## Monitoring & Observability

- **Health Checks**: Built-in `/health` endpoint
- **Logging**: Structured logging with request/response details
- **Metrics**: FastAPI automatic metrics collection
- **Error Handling**: Comprehensive error responses with details

## Security Considerations

- **Input Validation**: Pydantic models for request validation
- **Error Handling**: No sensitive information in error responses
- **Container Security**: Minimal base image with no unnecessary packages
- **Network Security**: Internal service communication only

## Future Enhancements

- **Custom Intent Models**: Fine-tuned models for specific business domains
- **Batch Processing**: Analyze multiple tickets simultaneously
- **Multi-language Support**: Extend beyond English text analysis
- **Real-time Streaming**: WebSocket support for live analysis
- **Model Versioning**: A/B testing with different model versions
- **Integration APIs**: Direct CRM system integrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Hugging Face Transformers**: For the excellent model ecosystem
- **CardiffNLP**: For the sentiment analysis model
- **FastAPI**: For the modern Python web framework
- **PyTorch**: For the deep learning framework