# Demeter LLM API
This API supports text and audio input, detects user intent, extracts relevant agroclimatic variables, and uses a RAG architecture to answer using AClimate data and LLaMA 3.

## Run the API
```bash
uvicorn src.api:app --reload
```

## Run the tests
```bash
pytest tests/
```

## Swagger UI
La documentación interactiva está disponible automáticamente en:
http://localhost:8000/docs
