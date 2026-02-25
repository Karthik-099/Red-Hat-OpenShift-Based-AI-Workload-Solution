# API Documentation

## Base URL

```
https://<route-url>
```

## Endpoints

### Health Check

Check service health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-inference"
}
```

**Status Codes:**
- 200: Service is healthy

### Readiness Check

Check if service is ready to accept requests.

**Endpoint:** `GET /ready`

**Response:**
```json
{
  "status": "ready",
  "model_loaded": true
}
```

**Status Codes:**
- 200: Service is ready

### Predict

Perform AI inference on input data.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
}
```

**Parameters:**
- data (array): Array of 10 float values

**Response:**
```json
{
  "prediction": -0.1234,
  "latency_ms": 12.34
}
```

**Response Fields:**
- prediction (float): Model prediction result
- latency_ms (float): Request processing time in milliseconds

**Status Codes:**
- 200: Success
- 400: Invalid input
- 500: Server error

**Example:**

```bash
curl -X POST https://<route-url>/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]}'
```

### Metrics

Prometheus metrics endpoint.

**Endpoint:** `GET /metrics`

**Response:** Prometheus text format

**Metrics Exposed:**
- inference_requests_total: Total number of inference requests
- inference_request_duration_seconds: Request duration histogram
- inference_errors_total: Total number of errors

**Example:**

```bash
curl https://<route-url>/metrics
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Input must have 10 features"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error message"
}
```

## Rate Limiting

No rate limiting is currently implemented. Consider implementing rate limiting for production use.

## Authentication

No authentication is currently required. Consider implementing authentication for production use.

## CORS

CORS is not configured. Configure as needed for web applications.
