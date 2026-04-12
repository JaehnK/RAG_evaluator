## 요청/응답 스키마 / Request/Response Schema

이 모듈은 외부 서버로 단일 POST 요청을 보냅니다.
The module sends a single POST request to an external server.

서버는 아래 형식의 요청 본문을 받고, 동일한 스키마로 응답해야 합니다.
The server should accept the request body and return a response in the format below.

### Request (JSON)
```json
{
  "question": "string",
  "top_k": 5
}
```

### Response (JSON)
```json
{
  "answer": "string",
  "contexts": [
    {
      "id": "doc_id",
      "text": "context chunk",
      "score": 0.91
    }
  ]
}
```
